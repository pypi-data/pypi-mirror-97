import numpy as np
import operator
from multiprocessing import Process, Pipe
from .DictEnv import EnvStatus, DictEnv, CloudpickleWrapper


def worker(remote, parent_remote, env_fn_wrapper, env_name):
    parent_remote.close()
    env = env_fn_wrapper.x(env_name)
    while True:
        cmd, data = remote.recv()
        if cmd == 'step':
            ob, reward, done, info = env.step(data)
            if done:
                ob = env.reset()
            remote.send((ob, reward, done, info))
        elif cmd == 'reset':
            ob = env.reset()
            remote.send(ob)
        elif cmd == 'seed':
            seed = env.seed(data)
            remote.send(seed)
        elif cmd == 'render':
            render_out = env.render(mode=data)
            remote.send(render_out)
        elif cmd == 'close':
            remote.close()
            break
        elif cmd == 'get_spaces':
            remote.send((env.observation_space, env.action_space))
        elif cmd == 'get_max_episode_steps':
            remote.send(env._max_episode_steps)
        else:
            raise NotImplementedError


class SubprocDictEnv(DictEnv):
    def __init__(self, observation_space=None, action_space=None):
        """
        envs: list of gym environments to run in subprocesses
        """
        self.status = {}
        self.waiting = False
        self.closed = False
        self.remotes, self.work_remotes = {}, {}
        self.ps = {}
        self.master_env_id = None
        self.observation_space = {}
        self.action_space = {}
        self._max_episode_steps = {}

        # check if observation_space and action_space are passed manually
        DictEnv.__init__(self)

    def add_env(self, env_fn, env_name):

        # get key for env instance
        try:
            env_id = str(max(map(int, self.status.keys())) + 1)
            assert env_id != self.master_env_id
        except ValueError:
            env_id = str(0)

        # place env in master if there is no other env
        if self.master_env_id == None:
            self.ps[env_id] = 'master'
            self.status[env_id] = EnvStatus.IDLE
            self.master_env_id = env_id

            # create env
            env = env_fn(env_name)
            self.observation_space[env_id] = env.observation_space
            self.action_space[env_id] = env.action_space
            self._max_episode_steps[env_id] = env._max_episode_steps
            self.remotes[env_id] = env

        else:  # start a new process and create an instance there
            # start a process
            remote, work_remote = Pipe()
            p = Process(target=worker, args=(work_remote, remote, CloudpickleWrapper(env_fn), env_name))

            self.remotes[env_id] = remote
            self.work_remotes[env_id] = work_remote
            self.ps[env_id] = p
            self.status[env_id] = EnvStatus.IDLE

            # start
            p.start()
            work_remote.close()

            # read observation_space, action_space and max_episode_steps
            self.remotes[env_id].send(('get_spaces', None))
            observation_space, action_space = self.remotes[env_id].recv()
            self.observation_space[env_id] = observation_space
            self.action_space[env_id] = action_space
            self.remotes[env_id].send(('get_max_episode_steps', None))
            max_episode_steps = self.remotes[env_id].recv()
            self._max_episode_steps[env_id] = max_episode_steps

        # increment self.num_envs
        self.inc_num(1)
        return env_id

    def step(self, actions):
        master_i = -1
        # for efficiency, send calls to remotes first and then run the master job
        for i in range(len(actions.env_id)):
            env_id = actions.env_id[i]
            if env_id != self.master_env_id:
                action = actions.data[i]
                self.remotes[env_id].send(('step', action))
                self.status[env_id] = EnvStatus.WAITING
            else:
                master_i = i

        # run the env on master
        if master_i != -1:
            env_id = actions.env_id[master_i]
            action = actions.data[master_i]
            master_result = self.remotes[env_id].step(action)
            self.status[env_id] = EnvStatus.IDLE

        # gather results
        results = []
        for i in range(len(actions.env_id)):
            env_id = actions.env_id[i]
            if env_id != self.master_env_id:
                results.append(self.remotes[env_id].recv())
                self.status[env_id] = EnvStatus.IDLE
            else:
                results.append(master_result)

        obs, rews, dones, infos = zip(*results)
        return obs, rews, dones, infos

    def reset(self, env_ids):
        reset_master = False
        for env_id in env_ids:
            if env_id != self.master_env_id:
                self.remotes[env_id].send(('reset', None))
            else:
                reset_master = True
        if reset_master:
            master_obs = self.remotes[self.master_env_id].reset()

        # gather observations
        results = []
        for env_id in env_ids:
            if env_id != self.master_env_id:
                results.append(self.remotes[env_id].recv())
            else:
                results.append(master_obs)
        return results

    def render(self, render_msgs):
        master_i = -1

        for i in range(len(render_msgs.env_id)):
            env_id = render_msgs.env_id[i]
            if env_id != self.master_env_id:
                mode = render_msgs.data[i]
                self.remotes[env_id].send(('render', mode))
                self.status[env_id] = EnvStatus.WAITING
            else:
                master_i = i

        # run the env on master
        if master_i != -1:
            env_id = render_msgs.env_id[master_i]
            mode = render_msgs.data[master_i]
            master_result = self.remotes[env_id].render(mode=mode)
            self.status[env_id] = EnvStatus.IDLE

        # gather results to make sure the render is finished on remotes
        results = []
        for i in range(len(render_msgs.env_id)):
            env_id = render_msgs.env_id[i]
            if env_id != self.master_env_id:
                results.append(self.remotes[env_id].recv())
                self.status[env_id] = EnvStatus.IDLE
            else:
                results.append(master_result)
        return results

    def seed(self, seeds_msgs):

        for i in range(len(seeds_msgs.env_id)):
            env_id = seeds_msgs.env_id[i]
            if env_id != self.master_env_id:
                seed = seeds_msgs.data[i]
                self.remotes[env_id].send(('seed', seed))
                self.status[env_id] = EnvStatus.WAITING
            else:
                env_id = seeds_msgs.env_id[i]
                seed = seeds_msgs.data[i]
                self.remotes[env_id].seed(seed)
                self.status[env_id] = EnvStatus.IDLE

        # gather results to make sure the seed is finished on remotes
        for i in range(len(seeds_msgs.env_id)):
            env_id = seeds_msgs.env_id[i]
            if env_id != self.master_env_id:
                self.remotes[env_id].recv()
                self.status[env_id] = EnvStatus.IDLE

    def close(self, env_ids):
        for env_id in env_ids:
            if self.status[env_id] == EnvStatus.WAITING and env_id != self.master_env_id:
                self.remotes[env_id].recv()

            if env_id != self.master_env_id:
                self.remotes[env_id].send(('close', None))
                self.ps[env_id].join()
            else:
                self.remotes[env_id].close()
                self.master_env_id = None
            del self.remotes[env_id]
            del self.ps[env_id]
            del self.status[env_id]

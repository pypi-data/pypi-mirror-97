import grpc
import numpy as np
import time

from sasrl_env.common.python.envp_pb2 import Actionsp, Namep, EnvIDsp, Emptyp

from sasrl_env.common.python.envp_pb2_grpc import EnvpStub


def decode_observation(observation):
    if not observation.data:
        return
    return np.asarray(observation.data).reshape(observation.shape)


class Object:
    pass


class Env:

    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.env_stub = EnvpStub(self.channel)
        self.envs = {}

    def make(self, name):
        info = self.env_stub.Makep(Namep(data=name))
        env_id = info.env_id
        self.envs[env_id] = Object()
        self.envs[env_id].observation_space = Object()
        self.envs[env_id].action_space = Object()
        self.envs[env_id].observation_space.shape = tuple(info.observation_shape)
        self.envs[env_id].action_space.n = info.num_actions
        self.envs[env_id]._max_episode_steps = info.max_episode_steps
        self.envs[env_id].env_id = env_id
        return env_id

    def reset(self, env_ids=None):
        if env_ids == None:
            env_ids = self.envs.keys()
        env_ids = EnvIDsp(data=env_ids)
        observations = self.env_stub.Resetp(env_ids)
        obs_lst = []
        for obs in observations.obs:
            obs_lst.append(decode_observation(obs))
        return obs_lst

    def step(self, action):

        env_id = []
        actions = []
        for k, v in action.items():
            env_id.append(k)
            actions.append(v)

        transition = self.env_stub.Stepp(Actionsp(env_id=env_id, data=actions))

        next_observations, rewards, dones = [], [], []
        for trans in transition.trans:
            next_observations.append(decode_observation(trans.next_observation))
            rewards.append(trans.reward)
            dones.append(trans.done)
        return next_observations, rewards, dones

    def Sample(self):
        action = self.env_stub.Samplep(Emptyp())
        return action

    def close(self, env_ids=None):
        if env_ids == None:
            env_ids = self.envs.keys
        self.env_stub.Closep(EnvIDsp(data=env_ids))


if __name__ == '__main__':
    host = '10.122.32.31'
    port = '10005'
    address = '{}:{}'.format(host, port)

    env = Env(address)
    # env.make('CartPole-v0')
    # env.make('Pong-v0')
    env_id = env.make('CartPole-v0')

    st = time.time()
    cnt = 0
    for i in range(100000):
        s = env.reset(env_ids = [env_id])
        cnt += 1
        action = {env_id: 1}
        done = [False]
        while not done[0]:
            ns, r, done = env.step(action)
            cnt += 1
            s = ns
            # report
            if cnt % 1000 == 0:
                print("cnt: {} -- rate: {}".format(cnt,cnt/(time.time()-st)))
    env.close([env_id])

    print('done')

    # cnt = 0
    # for i in range(100):
    #     s = env.reset()
    #     cnt += 1
    #     done = False
    #     while not done:
    #         ns, r, done = env.step(1)
    #         cnt += 1
    #         s = ns
    #         # report
    #         if cnt % 100 == 0:
    #             print("cnt: {} -- rate: {}".format(cnt,cnt/(time.time()-st)))
    # env1.close()

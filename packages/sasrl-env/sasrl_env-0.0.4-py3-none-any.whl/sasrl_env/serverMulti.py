from concurrent import futures
import argparse
import warnings
# get installed package starting with gym prefix
import pkg_resources
import grpc
from sasrl_env.env_dict.SubProcDict import SubprocDictEnv
import os

from sasrl_env.common.python.envp_pb2 import Infop, Observationp, Observationsp, Transitionp, Transitionsp, \
    Actionsp, Emptyp, RenderOutsp, RGBArryp
from sasrl_env.common.python.envp_pb2_grpc import EnvpServicer as Servicep, add_EnvpServicer_to_server as registerp

import gym

import logging
logger = logging.getLogger()



def make_env(env_name):
    env = gym.make(env_name)
    return env


def encode_observation(observation):
    return Observationp(data=observation.ravel(), shape=observation.shape)


class Envp(Servicep):
    env = SubprocDictEnv()

    def Makep(self, name, _):
        name = name.data
        env_id = self.env.add_env(make_env, name)
        logger.info('env {} with id {} created'.format(name, env_id))

        # check validity of observation_space
        try:
            self.env.observation_space[env_id]
        except:
            raise NameError('Environment should have an observation_space object. Use either Box or Discrete to define the space object.')

        try:
            if self.env.observation_space[env_id].__class__ == gym.spaces.box.Box:
                observation_space_type = 'box'
            elif self.env.observation_space[env_id].__class__ == gym.spaces.Discrete:
                observation_space_type = 'discrete'
        except:
            observation_space_type = 'none'

        # check validity of action_space
        try:
            self.env.action_space[env_id]
        except:
            raise NameError('Environment should have an action_space object of type Discrete.')

        if self.env.action_space[env_id].__class__ != gym.spaces.Discrete:
            action_space_type_ = "continues"
            raise NotImplementedError('Discrete is the only supported space for action_space.')
        else:
            num_actions = self.env.action_space[env_id].n
            action_space_type_ = "discrete"

        return Infop(observation_space_type=observation_space_type,
                     observation_shape=self.env.observation_space[env_id].shape,
                     num_actions=self.env.action_space[env_id].n,
                     max_episode_steps=self.env._max_episode_steps[env_id],
                     action_space_type=action_space_type_,
                     env_id=env_id)

    def Resetp(self, env_ids, _):
        obs = self.env.reset(env_ids.data)
        env_obs = [encode_observation(ob) for ob in obs]
        obs = Observationsp(obs=env_obs)
        return obs

    def Stepp(self, actions, _):

        next_observations, rewards, dones, _ = self.env.step(actions)
        transitions = []
        for i in range(len(next_observations)):
            next_obs = encode_observation(next_observations[i])
            transitions.append(Transitionp(next_observation=next_obs,
                                           reward=rewards[i],
                                           done=dones[i]))
        return Transitionsp(trans=transitions)

    def Samplep(self, env_ids, _):
        # todo: test this function
        action = self.env.action_space.sample()
        return Actionsp(data=action)

    def Renderp(self, renders, _):
        res = self.env.render(renders)

        mode = renders.data
        if mode == 'rgb_array':
            reno = RenderOutsp(rgb_array=[RGBArryp(rgb=r.flatten()) for r in res])
        elif mode == 'ansi':
            reno = RenderOutsp(ansi=res)
        elif mode == 'human':
            reno = RenderOutsp()
        else:
            raise Exception("render mode {} not supported.".format(mode))

        return reno

    def Seedp(self, seeds, _):
        if hasattr(self.env, 'seed'):
            self.env.seed(seeds)
        else:
            logger.warning("There is no function to set seed in the environment.")
        return Emptyp()

    def Closep(self, env_ids, _):
        self.env.close(env_ids.data)
        return Emptyp()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('environment server')
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=str)
    parser.add_argument('--get_pid', type=bool, default=True)

    args = parser.parse_args()

    if args.get_pid:
        pid = os.getpid()
        file1 = open(".pid.txt", "w")
        file1.writelines(str(pid))
        file1.close()

    address = '{}:{}'.format(args.host, args.port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    registerp(Envp(), server)
    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()

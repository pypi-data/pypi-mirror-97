import gym
from sasrl_env.common.python.env_pb2 import Info, Observation, Transition, Action, Empty, RenderOut, MetaData
from sasrl_env.common.python.env_pb2_grpc import EnvServicer as Service

from sasrl_env.common.python.utils import get_logger
import logging
logger = logging.getLogger()

def encode_observation(observation):
    return Observation(data=observation.ravel(), shape=observation.shape)

class Env(Service):
    def Handshake(self, empty, _):
        # set the version manually
        version = "0.0.2"
        return MetaData(EnvVersion=version)

    def Make(self, name, _):
        name = name.data
        if not hasattr(self, 'env') or self.env.spec.id != name:
            self.env = gym.make(name)
        logger.info('env {} created'.format(name))

        # check validity of observation_space
        try:
            self.env.observation_space
        except:
            raise NameError('Environment should have an observation_space object. Use either Box or Discrete to define the space object.')

        try:
            if self.env.observation_space.__class__ == gym.spaces.box.Box:
                observation_space_type = 'box'
            elif self.env.observation_space.__class__ == gym.spaces.Discrete:
                observation_space_type = 'discrete'
        except:
            raise NotImplementedError('Box and Discrete are the only supported observation_space types.')

        # check validity of action_space
        try:
            self.env.action_space
        except:
            raise NameError('Environment should have an action_space object of type Discrete.')

        if self.env.action_space.__class__ != gym.spaces.Discrete:
            action_space_type_ = "continues"
            num_actions = 0
            logger.warning('Discrete is the only supported space for action_space.')
        else:
            num_actions = self.env.action_space.n
            action_space_type_ = "discrete"

        return Info(observation_space_type=observation_space_type,
                    observation_shape=self.env.observation_space.shape,
                    num_actions=num_actions,
                    max_episode_steps=self.env._max_episode_steps,
                    action_space_type=action_space_type_)

    def Reset(self, empty, _):
        return encode_observation(self.env.reset())

    def Step(self, action, _):
        next_observation, reward, done, _ = self.env.step(action.data)
        next_observation = encode_observation(next_observation)
        return Transition(next_observation=next_observation,
                          reward=reward,
                          done=done)


    def Render(self, rendermode, _):
        res = self.env.render(rendermode.data)

        mode = rendermode.data
        if mode == 'rgb_array':
            reno = RenderOut(rgb_array=res.flatten())
        elif mode == 'ansi':
            reno = RenderOut(ansi=res)
        elif mode == 'human':
            reno = RenderOut()
        else:
            raise Exception("render mode {} not supported.".format(mode))

        return reno

    def Sample(self, empty, _):
        action = self.env.action_space.sample()
        return Action(data=action)

    def Close(self, empty, _):
        self.env.close()
        return Empty()

    def Seed(self, EnvSeed_, _):
        if hasattr(self.env, 'seed'):
            self.env.seed(EnvSeed_.data)
        else:
            logger.warning("There is no function to set seed in the environment.")
        return Empty()

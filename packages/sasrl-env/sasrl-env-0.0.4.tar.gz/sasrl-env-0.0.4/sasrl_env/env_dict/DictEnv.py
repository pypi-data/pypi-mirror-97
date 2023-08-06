from abc import ABC, abstractmethod
from enum import Enum


# code obtained from
# https://github.com/openai/baselines/blob/9cb7ece3387c4cb680fd831f38400b356bd599a6/baselines/common/vec_env/__init__.py

class EnvStatus(Enum):
    IDLE = 1
    WAITING = 2
    CLOSED = 3


class DictEnv(ABC):
    """
    Abstract class for asynchronous environments.
    """

    def __init__(self):
        self.num_envs = 0

    def inc_num(self, n=1):
        self.num_envs += n

    @abstractmethod
    def close(self, env_ids):
        """
        Clean up the environments' resources.
        """
        pass

    @abstractmethod
    def step(self, actions):
        """
        Do asynchoronous update in selected environments
        :param actions: a dict of environment ids with the actions in each
        Returns (obs, rews, dones, infos):
         - obs: an array of observations, or a tuple of
                arrays of observations.
         - rews: an array of rewards
         - dones: an array of "episode done" booleans
         - infos: a sequence of info objects
        """
        pass

    def render(self):
        print('Render not defined for %s' % self)

    @property
    def unwrapped(self):
        if isinstance(self, DictEnvWrapper):
            return self.denv.unwrapped
        else:
            return self


class DictEnvWrapper(DictEnv):
    def __init__(self, denv, observation_space=None, action_space=None):
        self.denv = denv
        DictEnv.__init__(self,
                         observation_space=observation_space or denv.observation_space,
                         action_space=action_space or denv.action_space)

    def step_async(self, actions):
        self.denv.step_async(actions)

    @abstractmethod
    def reset(self, env_ids):
        pass

    @abstractmethod
    def step_wait(self, actions):
        pass

    def close(self, env_ids):
        return self.denv.close(env_ids)

    def render(self):
        self.denv.render()


class CloudpickleWrapper(object):
    """
    Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
    """

    def __init__(self, x):
        self.x = x

    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)

    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)

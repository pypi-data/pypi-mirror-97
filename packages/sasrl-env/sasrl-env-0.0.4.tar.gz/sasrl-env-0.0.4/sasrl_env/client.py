import grpc
import numpy as np

from sasrl_env.common.python.env_pb2 import Action, Empty, Name
from sasrl_env.common.python.env_pb2_grpc import EnvStub

def decode_observation(observation):
    if not observation.data:
        return
    return np.asarray(observation.data).reshape(observation.shape)

class Object:
    pass

class Env:

    def __init__(self, name, address):
        self.channel = grpc.insecure_channel(address)
        self.env = EnvStub(self.channel)
        self.make(name)

    def make(self, name):
        info = self.env.Make(Name(data=name))
        self.observation_space = Object()
        self.action_space = Object()
        self.observation_space.shape = tuple(info.observation_shape)
        self.action_space.n = info.num_actions
        self._max_episode_steps = info.max_episode_steps

    def reset(self):
        return decode_observation(self.env.Reset(Empty()))

    def step(self, action):
        transition = self.env.Step(Action(data=action))
        next_observation = decode_observation(transition.next_observation)
        return next_observation, transition.reward, transition.done

    def Sample(self):
        action = self.env.Sample(Empty())
        return action
    def Close(self):
        self.env.Close()

    def close(self):
        self.channel.close()

if __name__ == '__main__':
    import time
    host = '10.122.32.31'
    port = '10005'
    address = '{}:{}'.format(host, port)

    # env = Env('Pong-v0', address)
    env = Env('CartPole-v0', address)

    st = time.time()
    cnt = 0
    for i in range(1000):
        s = env.reset()
        cnt += 1
        done = False
        while not done:
            ns, r, done = env.step(1)
            cnt += 1
            s = ns
            # report
            if cnt % 100 == 0:
                print("cnt: {} -- rate: {}".format(cnt,cnt/(time.time()-st)))
    env.close()
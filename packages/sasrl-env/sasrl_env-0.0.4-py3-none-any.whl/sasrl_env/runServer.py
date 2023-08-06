import argparse
from sasrl_env.gymServer import start

if __name__ == '__main__':
    parser = argparse.ArgumentParser('environment server')
    parser.add_argument('--port', type=int, default=10005)
    parser.add_argument('--mode', type=str, default="single")
    args = parser.parse_args()

    start(args.port, args.mode)

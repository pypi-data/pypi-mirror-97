from concurrent import futures
import socket
import argparse
import grpc

# get installed package starting with gym prefix
import pkg_resources

from sasrl_env.common.python.env_pb2_grpc import EnvServicer as Service, \
    add_EnvServicer_to_server as register
from sasrl_env.serverSingle import Env
from sasrl_env.common.python.envp_pb2_grpc import EnvpServicer as Servicep, \
    add_EnvpServicer_to_server as registerp
from sasrl_env.serverMulti import Envp

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                  for i in installed_packages
                                  if (i.key.startswith('gym') or i.key.endswith('gym'))])

from sasrl_env.common.python.utils import get_logger
logger = get_logger(log_level='info')
logger.info("Available gym packages: " + str(installed_packages_list))

# gym packages to import
import gym

modules = sorted(["%s" % i.key.replace('-', '_')
                  for i in installed_packages
                  if ((i.key.startswith('gym') or i.key.endswith('gym')) and (i.key != 'gym'))])
for library in modules:
    try:
        exec("import {module}".format(module=library))
    except Exception as e:
        print(e)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class register_server():
    def start(self, port, mode='single', max_threads=8):
        host = get_ip()
        address = '{}:{}'.format(host, port)
        if mode == 'single':
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
            register(Env(), server)
        elif mode == 'multi':
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_threads))
            registerp(Envp(), server)

        server.add_insecure_port(address)
        server.start()
        logger.info("started server at: {}".format(address))
        server.wait_for_termination()
        return 0

def start(port, mode='single'):
    rs = register_server()
    rs.start(port, mode)
    return 0



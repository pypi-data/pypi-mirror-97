# sasrl-env

## Overview
Generate protobuf files in python and C++ to be used for remote access to RL environment.

### Installation
-First, the sasrl-env package needs to be installed using the following command:
  - pip install sasrl-env

-Second, in the python environment, the installed package needs to be imported and started using the following lines of codes:
  - from sasrl_env import gymServer
  - gymServer.start('YOUR_PORT_NUMBER', mode = 'MODE') # MODE is either 'single', or 'multi' which are used to start one server or multiple servers (for parallel processing), respectively.

## Contributing
> We welcome your contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit contributions to this project.

## License
> This project is licensed under the [Apache 2.0 License](LICENSE).

## Supported version:
* protoc 3.13.0
* grpc 1.34.1

## Additional Resources
* Documentation links
* Blog posts
* SAS Communities

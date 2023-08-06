import os

import yaml
from polidoro_argument import Command

from polidoro_cli.cli import CLI, CLI_DIR, set_environment_variables, CONFIG_FILE


class UnifiedDockerCompose(CLI):
    help = 'UnifiedDockerCompose CLI commands'

    @staticmethod
    @Command(help='Add a folder in the Unified Docker Compose universe')
    def add(folder_path):
        try:
            os.chdir(folder_path)
            full_path = os.getcwd()
            if not os.path.exists('docker-compose.yml'):
                print('Folder must have a "docker.compse.yml" file')
                exit(1)
        except FileNotFoundError as fnf:
            print(fnf)
            exit(1)

        folders = UnifiedDockerCompose._get_udc_folders()
        folders += [full_path]
        set_environment_variables(
                            'UNIFIED_DOCKER_COMPOSE_FOLDERS',
                            ','.join(set(folders)),
                            file_name=CONFIG_FILE,
                            verbose=False,
                            exit_on_complete=False)
        print('Folder "%s" successfully added to Unified Docker Compose!' % full_path)

    @staticmethod
    def create_docker_compose():
        def fix_path(_config, key):
            last_dict = _config
            last_key = key.split('.')[-1]
            for k in key.split('.')[:-1]:
                last_dict = last_dict.get(k, {})
            if last_key in last_dict:
                last_dict[last_key] = os.path.join(os.getcwd(), last_dict[last_key])

        services = {}
        volumes = {}
        for folder in UnifiedDockerCompose._get_udc_folders():
            os.chdir(folder)

            if os.path.exists('docker-compose.yml'):
                with open('docker-compose.yml') as file:
                    try:
                        compose = yaml.safe_load(file)
                        compose.pop('networks', None)
                        for service, config in compose['services'].items():
                            config.pop('networks', None)

                            # Fixing paths
                            fix_path(config, 'build.context')
                            fix_path(config, 'env_file')

                            # Fixing volumes paths
                            config_volumes = []
                            for volume in config.get('volumes', []):
                                name, sep, path = volume.partition(':')
                                if name not in compose.get('volumes', {}):
                                    name = os.path.join(os.getcwd(), name)
                                config_volumes.append(name + sep + path)

                            config['volumes'] = config_volumes

                            services[service] = config

                        for volume, config in compose.get('volumes', {}).items():
                            if config is None:
                                config = {}

                            external = config.get('external', {})
                            external_name = external.get('name', '%s_%s' % (folder.split('/')[-1], volume))

                            external['name'] = external_name
                            config['external'] = external
                            volumes[volume] = config

                    except yaml.YAMLError as exc:
                        print(exc)

        final_compose = {
            'version': '3.6',
            'services': services,
            'volumes': volumes
        }
        with open(os.path.join(CLI_DIR, 'unified-docker-compose.yml'), 'w') as final_compose_file:
            yaml.dump(final_compose, final_compose_file)

    @staticmethod
    @Command(
        help='Run "docker-compose up"'
    )
    def up(*args):
        UnifiedDockerCompose.create_docker_compose()
        docker_compose = os.path.join(CLI_DIR, 'unified-docker-compose.yml')
        CLI.execute('docker-compose -f %s up %s' % (docker_compose, ' '.join(args)))
        # print(CLI_DIR)

    @staticmethod
    def _get_udc_folders():
        folders = os.environ.get('UNIFIED_DOCKER_COMPOSE_FOLDERS', [])
        if not isinstance(folders, list):
            folders = folders.split(',')

        return folders

#
#     @staticmethod
#     @Command(
#         help='Run "docker-compose up"'
#     )
#     def up(*args):
#         compose_args, other_args = Docker.split_args(args)
#         udc_dir = UnifiedDockerCompose._get_udc_dir()
#         CLI.execute('docker-compose up %s %s %s' % (compose_args, Docker.get_container_name(), other_args),
#                     dir=udc_dir)
#
#     @staticmethod
#     @Command(
#         help='Run "docker-compose down"'
#     )
#     def down(*args):
#         compose_args, other_args = Docker.split_args(args)
#         udc_dir = UnifiedDockerCompose._get_udc_dir()
#         CLI.execute('docker-compose down %s %s' % (compose_args, other_args),
#                     dir=udc_dir)
#
#     @staticmethod
#     @Command(
#         help='Restart the container'
#     )
#     def restart(*args):
#         Docker.stop()
#         UnifiedDockerCompose.up(*args)
#
#     @staticmethod
#     def _get_udc_dir():
#         udc_dir = os.environ.get('UNIFIED_DOCKER_COMPOSE_DIR', None)
#         if udc_dir and not os.path.exists(udc_dir):
#             print('%s is not a valid directory' % udc_dir)
#             udc_dir = None
#         if not udc_dir:
#             udc_dir = set_environment_variables(
#                 'UNIFIED_DOCKER_COMPOSE_DIR',
#                 input('Unified Docker Compose dir: '),
#                 file_name=CONFIG_FILE,
#                 exit_on_complete=False)
#         return udc_dir
#

# UnifiedDockerCompose()
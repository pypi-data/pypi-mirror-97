import os
from string import Template

from polidoro_argument import Command
from polidoro_cli.cli import CLI


class Docker(CLI):
    help = 'Docker CLI commands'
    _container_name = None

    def __init__(self):
        super(Docker, self).__init__(
            commands={
                'ps': 'docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"',
                'bash': 'docker exec -it $container bash',
                'stop': 'docker stop $container',
                'logs': 'docker logs $container',
                'up': 'docker-compose up',
                'down': 'docker-compose down',
            },
        )

    @classmethod
    def wrapper(cls, name, cmd, **kwargs):
        def wrapper_(*args, **_kwargs):
            kwargs.update(_kwargs)
            final_cmd = Template(cmd).safe_substitute(container=Docker.get_container_name())
            Docker.execute(final_cmd, *args, **kwargs)

        setattr(wrapper_, '__name__', name)
        return wrapper_

    @staticmethod
    def get_container_name():
        if Docker._container_name is None:
            container_name_key = os.getcwd() + '_CONTAINER_NAME'
            Docker._container_name = os.getenv(container_name_key, os.getcwd().split('/')[-1])
        return Docker._container_name

    @staticmethod
    @Command(
        help='Run "docker exec COMMAND"',
        aliases={'environment_vars': 'e'}
    )
    def exec(*args, environment_vars={}):
        if isinstance(environment_vars, str):
            env_vars = environment_vars
        else:
            env_vars = ' '.join('%s=%s' % (key, value) for key, value in environment_vars.items())

        if env_vars:
            env_vars = ' -e ' + env_vars
        return CLI.execute('docker exec%s -it %s %s' % (
            env_vars,
            Docker.get_container_name(),
            ' '.join(args)
        ))

    @staticmethod
    @Command(
        help='Run "docker run"'
    )
    def run(*args):
        run_args, other_args = Docker.split_args(args)
        container_name = Docker.get_container_name()
        run_args += " -v %s:/%s" % (os.getcwd(), container_name)
        run_args += " --network %s" % container_name
        run_args += " -it"
        CLI.execute('docker run %s %s %s' % (run_args, container_name, other_args))

    @staticmethod
    def split_args(args):
        compose_args = ' '.join(filter(lambda a: a.startswith('-'), args))
        other_args = ' '.join(filter(lambda a: not a.startswith('-'), args))
        return compose_args, other_args


Docker()

"""
Module doc sctring
"""
import os

from polidoro_argument import Command

from polidoro_cli.cli import set_environment_variables, CONFIG_FILE


class CLI:
    """
    Parent class for CLI classes
    """

    def __init__(self, commands=None, aliases=None, helpers=None, command_help=None):
        if commands is None:
            commands = {}
        if aliases is None:
            aliases = {}
        if helpers is None:
            helpers = {}
        if command_help is None:
            command_help = {}
        for name, cmd in commands.items():
            if isinstance(cmd, dict):
                kwargs = cmd
            else:
                kwargs = {'cmd': cmd}

            Command(
                aliases=aliases,
                helpers=helpers,
                help=command_help.get(name, 'Run "%s"' % kwargs['cmd']),
                method_name=name
            )(self.__class__.wrapper(name, **kwargs))

    @classmethod
    def wrapper(cls, name, cmd, **kwargs):
        raise NotImplemented

    @classmethod
    def execute(cls, command, *args, docker=False, environment_vars=None, folder=None):
        if environment_vars is None:
            environment_vars = {}
        command = ' '.join([command] + list(args))
        if docker:
            from polidoro_cli.clis.docker import Docker
            return Docker.exec(command, environment_vars=environment_vars)
        else:
            cur_dir = os.getcwd()
            try:
                if environment_vars:
                    command = ' '.join(
                        ['%s=%s' % (name, value) for name, value in environment_vars.items()] + [command]
                    )
                print('+ %s' % command + ('' if folder is None else ' in %s' % folder))
                if folder:
                    os.chdir(folder)
                return os.system(command)
            finally:
                os.chdir(cur_dir)

    @staticmethod
    @Command()
    def set_environment_variables(*args):
        for env in args:
            key, _, value = env.partition("=")
            set_environment_variables(key, value, CONFIG_FILE)

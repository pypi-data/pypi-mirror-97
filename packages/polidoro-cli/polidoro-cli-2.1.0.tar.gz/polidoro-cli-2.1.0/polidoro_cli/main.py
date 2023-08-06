# TODO
# bash completion
import glob
import os
import sys
from subprocess import CalledProcessError

from polidoro_argument import ArgumentParser

from polidoro_cli.cli.cli_utils import load_environment_variables, CONFIG_FILE, LOCAL_ENV_FILE, change_to_clis_dir, \
    get_clis_dir

load_environment_variables(CONFIG_FILE)
load_environment_variables(LOCAL_ENV_FILE)

VERSION = '2.1.0'


def load_clis(cli_dir):
    sys.path.append(cli_dir)
    for file in os.listdir(cli_dir):
        if os.path.isfile(os.path.join(cli_dir, file)) and not file.startswith('__') and file.endswith('.py'):
            __import__(file.replace('.py', ''))


def load_default_clis():
    load_clis(get_clis_dir())


def load_custom_clis():
    custom_cli_path = os.environ.get("CUSTOM_CLI_PATH")
    if custom_cli_path:
        load_clis(os.path.expanduser(custom_cli_path))


def main():
    # Load CLIs
    load_default_clis()
    load_custom_clis()

    try:
        ArgumentParser(version=VERSION).parse_args()
    except CalledProcessError as error:
        return error.returncode
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    os.environ['CLI_PATH'] = os.path.dirname(os.path.realpath(__file__))

    main()

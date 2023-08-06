# TODO
# bash completion
import glob
import os
from subprocess import CalledProcessError

from polidoro_argument import ArgumentParser

from polidoro_cli.cli.cli_utils import load_environment_variables, CONFIG_FILE, LOCAL_ENV_FILE, change_to_clis_dir, \
    get_clis_dir

load_environment_variables(CONFIG_FILE)
load_environment_variables(LOCAL_ENV_FILE)

VERSION = '2.0.0-RC'


def load_clis():
    cur_dir = os.getcwd()
    change_to_clis_dir()
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('__'):
            try:
                os.chdir(d)
                for file in glob.glob('*.py'):
                    __import__('polidoro_cli.clis.%s.%s' % (d, file.replace('.py', '')))
            except SystemExit as e:
                print(e)
        change_to_clis_dir()
    os.chdir(cur_dir)

def new_load_clis():
    clis_dir = get_clis_dir()
    for file in os.listdir(clis_dir):
        if os.path.isfile(os.path.join(clis_dir, file)) and not file.startswith('__'):
            __import__('polidoro_cli.clis.' + file.replace('.py', ''))
    # os.environ['PYTHONPATH'] = "/home/heitor/workspace/cli/:/home/heitor/workspace"
    # print(os.environ['PYTHONPATH'])
    # change_to_clis_dir()
    # os.environ['PYTHONPATH'] = '/home/heitor/workspace/local_clis'
    # os.chdir('/home/heitor/workspace')
    # __import__('local_clis.teste')
    # os.chdir('/home/heitor/workspace/cli/polidoro_cli')
    # __import__('polidoro_cli.clis.elixir2')
    # Elixir2()
    # __import__('elixir2')
    # for file in os.listdir():
        # if os.path.isfile(file) and not file.startswith('__'):
        #     print(file)

def main():
    # Load all the CLIs
    # load_clis()
    new_load_clis()

    try:
        ArgumentParser(version=VERSION).parse_args()
    except CalledProcessError as error:
        return error.returncode
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    os.environ['CLI_PATH'] = os.path.dirname(os.path.realpath(__file__))

    main()

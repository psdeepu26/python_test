import sys
import os
import site


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BFAIL = BOLD + FAIL
    UNDERLINE = '\033[4m'


def mod_install(cmd, module):
    try:
        __import__(module)
    except ImportError as err:
        print bcolors.OKBLUE + str(err) + " " + "Installing it now...".format(module) + bcolors.ENDC
        os.system(cmd)
        reload(site)


def validate_pip():
    try:
        __import__('pip')
    except ImportError:
        print bcolors.BFAIL + "pip not found, Please install pip before proceeding." + bcolors.ENDC
        sys.exit(1)


if __name__ == '__main__':
    filename = "setup/requirements.txt"
    mod_list = [mod.rstrip('\n') for mod in open(filename)]
    validate_pip()
    for modules in mod_list:
        cmd = "sudo pip install " + modules
        mod_install(cmd, modules)
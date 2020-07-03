import sys
import argparse
import time
import boto3
from boto3.exceptions import botocore
__version__ = "1.0.0"

class bcolors:
    """Setting Text ForeGround Color"""
    BOLD = '\033[1m'
    HEADER = '\033[95m' + BOLD
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m' + BOLD
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    OK = BOLD + OKGREEN + u'\u2705' + "  "
    ERR = BOLD + FAIL + u"\u274C" + "  "
    WAIT = BOLD + OKBLUE + u'\u231b' + "  "
    HELP = OKBLUE
    BHELP = FAIL + BOLD
    BMSG = BOLD + OKBLUE
    DONE = BOLD + "Done " + u"\u2705"

def description():
    '''
    Santhosh Deepu Patrayuni
    '''

def parseCmdLineArgs():
    global __version__
    parser = argparse.ArgumentParser(description=description.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-p", "--profile", action="store", dest="aws_profile", required=True, help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "AWS Profile Name as in ~/.aws/credentials" + bcolors.ENDC)
    parser.add_argument("-r", "--region", action="store", dest="aws_region", required=True, help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "AWS Region" + bcolors.ENDC)
    args = vars(parser.parse_args())
    print(args)
    return args

def main(args):
    aws_profile = args['aws_profile']
    aws_region = args['aws_region']
    valid_aws_region = ['us-west-2', 'us-east-1']

    if aws_region not in valid_aws_region:
        print(bcolors.ERR,'Invalid AWS Region passed. Valid values are {}'.format(valid_aws_region),bcolors.ENDC)
        exit(1)
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

if __name__ == '__main__':
    start_time = time.time()
    args = parseCmdLineArgs()
    try:
        main(args)
    except KeyboardInterrupt:
        print("")
        print(bcolors.ERR,'User Interruption received. Existing...',bcolors.ENDC)
    except botocore.exceptions.ProfileNotFound:
        print(bcolors.ERR + 'Profile {} not found in ~/.aws/credentials.'.format(args['aws_profile']) + bcolors.ENDC)
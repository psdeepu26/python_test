import boto3
import os
import argparse
import sys
from texttable import Texttable

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

def list_instances(search,profilename):
    try:
        current_profile = os.environ['AWS_DEFAULT_PROFILE']
    except:
        current_profile = ""
    if profilename:
        Profile_Session = boto3.session.Session(profile_name=profilename)
        client = Profile_Session.client('ec2')
        Profilename = Profile_Session.profile_name
    elif current_profile:
        client = boto3.client('ec2')
        Profilename = boto3.session.profile_name
    else:
        print(bcolors.WARNING,"Profile argument is not given and Currently you are not logged into any profile, hence can't proceed and exiting the script",bcolors.ENDC)
        sys.exit()

    responses = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ]
    )
    Account_ID = responses['Reservations'][0]['OwnerId']
    print('\x1b[6;30;42m',bcolors.BOLD,"Current Profile Name : ",Profilename,"\t\t","Current Account ID: ",Account_ID,bcolors.ENDC,'\x1b[0m')
    InstanceList = []
    TagsList = []
    idx = 1

    InstanceList = [['SL No.', 'InstanceName',  'InstanceId', 'PrivateIPAddress']]
    for response in responses['Reservations']:
        for Tag in response['Instances'][0]['Tags']:
            if (Tag['Key'] == 'Name'):
                if search in Tag['Value']:
                    InstanceList.append([idx, Tag.get('Value','NoName'), response['Instances'][0]['InstanceId'], response['Instances'][0]['PrivateIpAddress']])
                    idx = idx + 1

    t = Texttable()
    t.add_rows(InstanceList)
    print(t.draw())
    return(InstanceList)


def login(file,InstanceList,Bastion,verbose):
    print("\n")
    choice = input("Enter SL No to login: ")
    choice_instance = InstanceList[int(choice)][3]
    if verbose:
        command = 'ssh -i '+file+' ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' ec2-user@'+Bastion+'"'
    else:
        command = 'ssh -i '+file+' ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' ec2-user@'+Bastion+'"'
    os.system(command)


def main():
    parser = argparse.ArgumentParser(description="Used for logging into the AWS Instances")
    parser.add_argument("-f", "--file", action="store", help="Provide Absolute path of the file",required=True)
    parser.add_argument("-b", "--bastion", action="store", help="Provide Bastion IP/FQDN",required=True)
    parser.add_argument("-p", "--profilename", action="store", help="Provide Profile Name",required=True)
    parser.add_argument("-s", "--searchstring", action="store", help="Provide Search String")
    parser.add_argument("-v", "--verbose", action="store_true", help="Versobe SSH")
    args = parser.parse_args()
    file = args.file
    Bastion = args.bastion
    Profile = args.profilename
    search = args.searchstring

    if not search:
        search = ""

    if(os.path.exists(file)):
        InstanceList = list_instances(search,Profile)
        login(file,InstanceList,Bastion,args.verbose)
    else:
        print("File doesn't exist, Exiting the Script")
        sys.exit()


if __name__ == '__main__':
    try:
       main()
    except KeyboardInterrupt:
        print('')
        print('\033[1m' + '\nKeyboard Interruption..Calm Down')
        print('\033[1m' + '\nExiting !!!!\n')
        print('\033[0m')
        sys.exit()
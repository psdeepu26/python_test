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

def list_instances(search,Bastion):
    client = boto3.client('ec2')
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

    InstanceList = []
    TagsList = []
    idx = 1

    InstanceList = [['SL No.', 'InstanceName',  'InstanceId', 'PrivateIPAddress','PublicIpAddress']]
    for response in responses['Reservations']:
        for Tag in response['Instances'][0]['Tags']:
            if (Tag['Key'] == 'Name'):
                if search in Tag['Value']:
                    InstanceList.append([idx, Tag.get('Value','NoName'), response['Instances'][0]['InstanceId'], response['Instances'][0]['PrivateIpAddress'], response['Instances'][0].get('PublicIpAddress','')])
                    idx = idx + 1
                if not Bastion and (Tag['Key'] == 'Name') and (Tag['Value'] == 'bastion'):
                    Bastion = response['Instances'][0]['PublicIpAddress']

    t = Texttable()
    t.add_rows(InstanceList)
    print(t.draw())
    return(InstanceList,Bastion)
#    if not Bastion:
#        return(InstanceList,Bastion1)
#    else:
#        return(InstanceList,Bastion)

def change_profile(profilename):
    learn = boto3.session.Session(profile_name=profilename)


def login(file,InstanceList,Bastion,verbose):
    print("\n")
    choice = input("Enter SL No to login: ")
    choice_instance = InstanceList[int(choice)][3]
    if verbose == "True" or verbose == "true":
        #command = 'ssh -i '+file+' ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' ec2-user@'+Bastion+'"'
        command = 'ssh -i '+file+' -v ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' -v ec2-user@'+Bastion+'"'
    else:
        command = 'ssh -i '+file+' -qt ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' -qt ec2-user@'+Bastion+'"'
    os.system(command)


def main():
    parser = argparse.ArgumentParser(description="Used for logging into the AWS Instances")
    parser.add_argument("-f", "--file", action="store", help="Provide Absolute path of the file",required=True)
    parser.add_argument("-b", "--bastion", action="store", help="Provide Bastion IP/FQDN")
    parser.add_argument("-p", "--profilename", action="store", help="Provide Profile Name")
    parser.add_argument("-s", "--searchstring", action="store", help="Provide Search String")
    parser.add_argument("-v", dest='boolean_t', action="store_true", default=False, help="Versobe SSH")
    args = parser.parse_args()
    file = args.file
    Bastion = args.bastion
    Profile = args.profilename
    search = args.searchstring

    change_profile(profilename)
    
    if not search:
        search = ""
    #if not verbose:
    #    verbose = "True"


    if(os.path.exists(file)):
        InstanceList,Bastion = list_instances(search,Bastion)
        login(file,InstanceList,Bastion,args.boolean_t)
    else:
        print(bcolors.WARNING,"File doesn't exist, Exiting the Script",bcolors.ENDC)
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
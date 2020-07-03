import boto3
import sys
import time

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

def SetRecordSet(profilename,HostedZoneId,SourceName,DeploymentName):
    Profile_Session = boto3.session.Session(profile_name=profilename)
    client = Profile_Session.client('route53')
    print(bcolors.HEADER,"CNAME Switch Started..")
    print(bcolors.OKBLUE,"Changing the Alias for CNAME:",SourceName,"to ",DeploymentName)
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=HostedZoneId,
            ChangeBatch={
                "Comment": "Blue/Green Deployment",
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": SourceName,
                            "Type": "CNAME",
                            "TTL": 300,
                            "ResourceRecords": [
                                {
                                    "Value": DeploymentName
                                },
                            ],
                        }
                    },
                ]
            }
        )
        print(bcolors.OKGREEN,"Updated the Alias for CNAME:",SourceName,"to ",DeploymentName)
        print(bcolors.HEADER,"CNAME Switch Completed..")
    except:
        print(bcolors.WARNING,"CNAME updation failed")


def GetRecordSet(profilename,HostedZoneId,SourceName):
    Profile_Session = boto3.session.Session(profile_name=profilename)
    client = Profile_Session.client('route53')
    response = client.list_resource_record_sets(
        HostedZoneId=HostedZoneId,
        StartRecordName=SourceName,
        StartRecordType='CNAME'
    )
    print(bcolors.BOLD,"--------------------------------------------------------------------------------------------------------------------")
    print(bcolors.HEADER,"Current value for ",SourceName," is ",response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value'])


def main():
    Profile_Name = sys.argv[1]
    HostedZoneId = sys.argv[2]
    SourceName = sys.argv[3]
    DeploymentName = sys.argv[4]
    SetRecordSet(Profile_Name,HostedZoneId,SourceName,DeploymentName)
    time.sleep(10)
    GetRecordSet(Profile_Name,HostedZoneId,SourceName)


if __name__ == '__main__':
    try:
       main()
    except KeyboardInterrupt:
        print('')
        print('\033[1m' + '\nKeyboard Interruption..Calm Down')
        print('\033[1m' + '\nExiting !!!!\n')
        print('\033[0m')
        sys.exit()
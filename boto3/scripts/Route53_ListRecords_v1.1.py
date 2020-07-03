import boto3
import sys

def GetRecordSet(profilename,HostedZoneId,SourceName):
    Profile_Session = boto3.session.Session(profile_name=profilename)
    client = Profile_Session.client('route53')
    response = client.list_resource_record_sets(
        HostedZoneId=HostedZoneId,
        StartRecordName=SourceName,
        StartRecordType='CNAME'
    )
    print("=-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-=")
    print("Current value for ",SourceName," is ",response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value'])
    print("=-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-=\n")

def main():
    Profile_Name = sys.argv[1]
    HostedZoneId = sys.argv[2]
    SourceName1 = sys.argv[3]
    SourceName2 = sys.argv[4]
    GetRecordSet(Profile_Name,HostedZoneId,SourceName1)
    GetRecordSet(Profile_Name,HostedZoneId,SourceName2)

if __name__ == '__main__':
    try:
       main()
    except KeyboardInterrupt:
        print('')
        print('\033[1m' + '\nKeyboard Interruption..Calm Down')
        print('\033[1m' + '\nExiting !!!!\n')
        print('\033[0m')
        sys.exit()
import boto3
import sys

def GetRecordSet(profilename,HostedZoneId,SourceName):
    Profile_Session = boto3.session.Session(profile_name=profilename)
    client = Profile_Session.client('route53')
    temp = SourceName.split("-",1)
    findName = temp[0]
    temp = SourceName.split(".")
    findEnv = temp[0].rsplit("-",1)
    findEnv = findEnv[1]
    response = client.list_resource_record_sets(
        HostedZoneId=HostedZoneId
    )
    print("=-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-=\n")
    for i in response['ResourceRecordSets']:
        if (i['Type']=='CNAME'):
            if findName in i['Name']:
                if 'prf' in i['Name']:
                    print("Current value for ",i['Name']," is ",i['ResourceRecords'][0]['Value'])
    print("\n=-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-=\n")

def main():
    Profile_Name = sys.argv[1]
    HostedZoneId = sys.argv[2]
    SourceName = sys.argv[3]
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
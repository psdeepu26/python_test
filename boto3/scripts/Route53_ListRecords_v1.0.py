import boto3

def GetRecords():
	Session = boto3.session.Session(profile_name='deepu_new')
	client = Session.client('route53')
	response = client.list_resource_record_sets(
	    HostedZoneId='ZY4X5YO84M8G3',
	    StartRecordName='fdpdocv2.ws.qal.learn.intuit.net.',
	    StartRecordType='CNAME'
	)
	print(response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value'])


def main():
	GetRecords()

if __name__ == '__main__':
    try:
       main()
    except KeyboardInterrupt:
        print('')
        print('\033[1m' + '\nKeyboard Interruption..Calm Down')
        print('\033[1m' + '\nExiting !!!!\n')
        print('\033[0m')
        sys.exit()
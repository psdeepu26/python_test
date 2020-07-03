import boto3
import os
import argparse
import sys
from texttable import Texttable

def list_instances(search):
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

	os.system('clear')
	InstanceList = [['ChoiceNo.', 'InstanceName',  'InstanceId', 'PrivateIPAddress']]

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
	choice = input("Enter your ChoiceNo.: ")
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
	parser.add_argument("-b", "--bastion", action="store", help="Provide Bastion",required=True)
	parser.add_argument("-p", "--profilename", action="store", help="Provide Profile Name")
	parser.add_argument("-s", "--searchstring", action="store", help="Provide Search String")
	parser.add_argument("-v", "--verbose", action="store", help="Versobe SSH")
	args = parser.parse_args()
	file = args.file
	Bastion = args.bastion
	Profile = args.profilename
	search = args.searchstring
	verbose = args.verbose
	if not search:
		search = ""
	if not verbose:
		verbose = "True"

	if(os.path.exists(file)):
		InstanceList = list_instances(search)
		login(file,InstanceList,Bastion,verbose)
	else:
		print("File doesn't exist, Exiting the Script")
		sys.exit()

if __name__ == '__main__':
	main()
	
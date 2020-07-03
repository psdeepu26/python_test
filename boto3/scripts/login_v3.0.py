import boto3
import os
import argparse
import sys
from texttable import Texttable

def list_instances():
	client = boto3.client('ec2')
	responses = client.describe_instances()

	InstanceList = []
	TagsList = []

	os.system('clear')
	InstanceList = [['ChoiceNo.', 'InstanceName',  'InstanceId', 'PrivateIPAddress', 'PublicIPAddress']]
	#print('ChoiceNo.'+"\t"+'Instance Name'+"\t"+'Instance Id'+"\t"+'PrivateIPAddress'+"\t"+'PublicIPAddress')

	for idx, response in enumerate(responses['Reservations'], start=1):
		InstanceList.append([idx, response['Instances'][0]['InstanceId'], response['Instances'][0]['PrivateIpAddress'], response['Instances'][0].get('PublicIpAddress','')])

		for Tag in response['Instances'][0]['Tags']:
			if (Tag['Key'] == 'Name'):
				TagsList.append(Tag.get('Value','NoName'))
#			if (Tag['Key'] == 'Name') and (Tag['Value'] == 'bastion'):
#				Bastion = response['Instances'][0]['PublicIpAddress']

	for i in range(len(TagsList)):
		InstanceList[i+1].insert(1, TagsList[i])

	#print(InstanceList)

	t = Texttable()
	t.add_rows(InstanceList)
	print(t.draw())

	return(InstanceList)

def login(file,InstanceList,Bastion):
	choice = input("Enter your ChoiceNo.: ")
	choice_instance = InstanceList[int(choice)][3]
	command = 'ssh -i '+file+' ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i '+file+' ec2-user@'+Bastion+'"'
	os.system(command)

def main():
	parser = argparse.ArgumentParser(description="Used for logging into the AWS Instances")
	parser.add_argument("-f", "--file", action="store", help="Provide Absolute path of the file")
	parser.add_argument("-b", "--bastion", action="store", help="Provide Bastion")
	parser.add_argument("-p", "--profilename", action="store", help="Provide Profile Name")
	args = parser.parse_args()
	file = args.file
	Bastion = args.bastion
	Profile = args.profilename

	if(os.path.exists(file)):
		InstanceList = list_instances()
		login(file,InstanceList,Bastion)
	else:
		print("File doesn't exist, Exiting the Script")
		sys.exit()

if __name__ == '__main__':
	main()
	
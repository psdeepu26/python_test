import boto3
import sys
import os
import time
from texttable import Texttable

def SG_Intuit_CIDR_SSH(profilename):
	#print("SG_Intuit_CIDR_SSH")
	#client = boto3.client('cloudformation')
	if profilename:
		Profile_Session = boto3.session.Session(profile_name=profilename)
		client = Profile_Session.client('cloudformation')
		Profilename = Profile_Session.profile_name
	else:
		print(bcolors.WARNING,"Profile argument is not given and Currently you are not logged into any profile, hence can't proceed and exiting the script",bcolors.ENDC)
		sys.exit()
	try:
		response = client.create_stack(
		    StackName='intuit-cidr-ingress-tcp-22',
		    TemplateURL='https://s3-us-west-2.amazonaws.com/286056532910-scripts/intuit-cidr-ingress.yml',
		    Parameters=[
		        {
		            'ParameterKey': 'Name',
		            'ParameterValue': 'intuit-cidr-ingress',
		        },
		        {
		            'ParameterKey': 'Port',
		            'ParameterValue': '22',
		        },
		        {
		            'ParameterKey': 'VpcId',
		            'ParameterValue': 'vpc-73703315',
		        },
		    ],
		)
		#print(response)
	except Exception as error:
		print(StackName," Stack is not created for the following reason")
		print(error)
		print("\n")
		delete = input("Do you like to Delete this existing Stack (y/N) : ")
		if delete == 'y' or delete == 'Y':
			delete_stack("intuit-cidr-ingress-tcp-22",profilename)
		sys.exit()
	print("Stack with Name \"intuit-cidr-ingress-tcp-22\" is created",)
	monitor_stack('intuit-cidr-ingress-tcp-22',profilename)


def SG_Intuit_CIDR_HTTP():
	print("SG_Intuit_CIDR_HTTP")

def SG_Intuit_CIDR_HTTPS():
	print("SG_Intuit_CIDR_HTTPS")

def SG_Intuit_APIGW_CIDR_HTTPS():
	print("SG_Intuit_APIGW_CIDR_HTTPS")

def monitor_stack(Stack_Name,profilename):
	if profilename:
		Profile_Session = boto3.session.Session(profile_name=profilename)
		client = Profile_Session.client('cloudformation')
		Profilename = Profile_Session.profile_name
	else:
		print(bcolors.WARNING,"Profile argument is not given and Currently you are not logged into any profile, hence can't proceed and exiting the script",bcolors.ENDC)
		sys.exit()
	try:
		while True:
			response = client.describe_stack_events(
				StackName=Stack_Name,
			)
			List = []
			List = [['Stack_Id', 'Stack_Name',  'Resource_Status', 'Resource_Status_Reason']]
			print(response['StackEvents'][0]['ResourceStatus'])
			List.append([response['StackEvents'][0]['StackId'],response['StackEvents'][0]['StackName'], response['StackEvents'][0]['ResourceStatus'], response['StackEvents'][0]['ResourceStatusReason']])
			t = Texttable()
			t.add_rows(List)
			print(t.draw())
			resp = client.describe_stacks(
				StackName=Stack_Name,
			)
			StackStatus = resp['Stacks'][0]['StackStatus']
			if StackStatus == 'ROLLBACK_COMPLETE' or StackStatus == 'CREATE_FAILED' or StackStatus == 'CREATE_COMPLETE':
				print("Current status of the Stack is ",StackStatus)
	except Exception as error:
		print(error)


def delete_stack(Stack_Name,profilename):
	if Stack_Name == '':
		Stack_Name = input("Enter the Stack Name : ")
	if profilename:
		Profile_Session = boto3.session.Session(profile_name=profilename)
		client = Profile_Session.client('cloudformation')
		Profilename = Profile_Session.profile_name
	else:
		print(bcolors.WARNING,"Profile argument is not given and Currently you are not logged into any profile, hence can't proceed and exiting the script",bcolors.ENDC)
		sys.exit()
	try:	
		response = client.delete_stack(
		    StackName=Stack_Name
		)
		print(Stack_Name," is deleted successfully")
	except Exception as error:
		print(error)
		print("Unable to delete stack - ",Stack_Name)

def main():
	Profile = sys.argv[1]
	while True:	
#		os.system('clear')
		print("1. Create Stack - Security Group with Intuit CIDR for SSH")
		print("2. Create Stack - Security Group with Intuit CIDR for HTTP")
		print("3. Create Stack - Security Group with Intuit CIDR for HTTPS")
		print("4. Create Stack - Security Group with Intuit API GW CIDR for HTTPS")
		print("5. Delete Stack of your Choice")
		print("6. Exit")
		print("\n")
		choice = input("Enter Your Choice : ")
		if choice == '1':
			SG_Intuit_CIDR_SSH(Profile)
			break
		elif choice == '2':
			SG_Intuit_CIDR_HTTP()
		elif choice == '3':
			SG_Intuit_CIDR_HTTPS()
		elif choice == '4':
			SG_Intuit_APIGW_CIDR_HTTPS()
		elif choice == '5':
			delete_stack('',Profile)
		elif choice == '6':
			print("Thank you for using the Script")
			break
		else:
			print("Wrong Choice")
			time.sleep('5')
			continue


if __name__ == '__main__' :
	try:
		main()
	except KeyboardInterrupt:
		print('')
		print('\033[1m' + '\nKeyboard Interruption..Calm Down')
		print('\033[1m' + '\nExiting !!!!\n')
		print('\033[0m')
		sys.exit()
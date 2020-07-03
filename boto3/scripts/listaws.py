import boto3
import os
import re
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

def listprofiles(home):
	idx = 1
	with open(home, 'r',encoding='utf-8') as file:
		for line in file:
			line = line.strip()
			if line.startswith('[') and line.endswith(']'):
				profiles.append([idx, line[1:-1], re.sub('aws_access_key_id=', '', (next(file)).strip()), re.sub('aws_secret_access_key=', '', (next(file)).strip())])
				idx += 1
				#aws_accesskey = re.sub('aws_access_key_id=', '', (next(file)).strip())
				#aws_sec_access = re.sub('aws_secret_access_key=', '', (next(file)).strip())
	
	templist = []
	for idx, profile in enumerate(profiles):
		templist.append(profiles[idx][:2])

	t = Texttable()
	t.add_rows(templist)
	print(t.draw())

def current_profile():
	client = boto3.client('ec2')
	responses = client.describe_instances()
	Account_ID = responses['Reservations'][0]['OwnerId']
	Proiflename = os.environ['AWS_DEFAULT_PROFILE']
	print('\x1b[6;30;42m',bcolors.BOLD,"Current Profile Name : ",Proiflename,"\t\t","Current Account ID: ",Account_ID,bcolors.ENDC,'\x1b[0m')


def profilelogin():
	print(profiles[int(choice)])
	command1 = 'export AWS_DEFAULT_PROFILE='+profiles[int(choice)][1]
	command2 = 'export AWS_DEFAULT_REGION="us-west-2"'
	command3 = 'export AWS_ACCESS_KEY_ID='+profiles[int(choice)][2]
	command4 = 'export AWS_SECRET_ACCESS_KEY='+profiles[int(choice)][3]
	os.environ["AWS_DEFAULT_PROFILE"] = profiles[int(choice)][1]
	os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
	os.environ["AWS_ACCESS_KEY_ID"] = profiles[int(choice)][2]
	print(os.environ['AWS_DEFAULT_PROFILE'])
	current_profile()


def main():
	os.system('clear')
	current_profile()
	global profiles
	global choice
	profiles = []
	profiles = [['SL. No.', 'Profile Name']]
	home = os.path.expanduser("~")
	awscred = home+"/.aws/credentials"
	if (os.path.exists(awscred)):
		listprofiles(awscred)
		print("\n")
		choice = input("Enter SL No. to Select Profile: ")
		print(choice)
		profilelogin()



if __name__ == '__main__':
    try:
       main()
    except KeyboardInterrupt:
        print('')
        print('\033[1m' + '\nKeyboard Interruption..Calm Down')
        print('\033[1m' + '\nExiting !!!!\n')
        print('\033[0m')
        sys.exit()

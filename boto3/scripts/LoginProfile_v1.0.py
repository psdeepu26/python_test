import boto3
import os
import sys
from texttable import Texttable

def profileLister(path):
	global profilelist
	expandedpath = os.path.expanduser(path)
	profilelist = [['Index', 'Profile']]
	i = 1
	if (os.path.exists(expandedpath)):
		with open(expandedpath) as file:
			for line in file:
				if line.startswith('['):
					profilelist.append([int(i),line[1:-2]])
					i += 1
		t = Texttable()
		t.add_rows(profilelist)
		print(t.draw())

def choice():
	global profilelist
	choice = input("Enter your choice : ")
	profilechoice = profilelist[int(choice)][1]
	print("Choice of the Profile choosen :",profilechoice,"\n\n")
	return(profilechoice)

def ProfileLogin(path,profilechoice):
	expandedpath = os.path.expanduser(path)
	with open(expandedpath) as file:
		for line in file:
			if profilechoice in line:
				access = file.readline().split("=")
				secret = file.readline().split("=")
	region="us-west-2"
	access_key=access[1]
	secret_key=secret[1]
	#boto3.setup_default_session(aws_access_key_id=access_key,aws_secret_access_key=secret_keyregion_name=region,profile_name=profilechoice)
	x = profilechoice+".sh"
	with open(x, 'w') as file1:
		file1.write("export AWS_DEFAULT_PROFILE="+profilechoice+"\n")
		file1.write("export AWS_DEFAULT_REGION="+region+"\n")
		file1.write("export AWS_ACCESS_KEY_ID="+access_key)
		file1.write("export AWS_SECRET_ACCESS_KEY="+secret_key+"\n")
		file1.close()
	os.system('clear')
	print("Please execute",profilechoice+".sh to login to the profile","\n\n")

def main():
	path = '~/.aws/credentials'
	profileLister(path)
	profilechoice = choice()
	ProfileLogin(path,profilechoice)

profilelist =[]

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('')
		print('\033[1m' + '\nKeyboard Interruption..Calm Down')
		print('\033[1m' + '\nExiting !!!!\n')
		print('\033[0m')
		sys.exit()

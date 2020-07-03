# This python script will check if a given file exists are not
# In this case i am trying to check if "~/.aws/credentials" file exists are not

import os
#import boto3

def main():
	path = "~/.aws/credentials"
	if (os.path.exists(os.path.expanduser(path))):
		print(path, "file exists")
	else:
		print(path, "doesn't exists")

if __name__ == '__main__':
	main()
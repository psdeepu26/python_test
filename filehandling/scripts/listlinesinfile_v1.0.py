#This script is used to list the lines in a file and also get only the required strings from each of the lines
#In this, we tried to get all the profile names under ~/.aws/credentials

import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
	path = '~/.aws/credentials'
	profilelist = []
	i = 1
	expandedpath = os.path.expanduser(path)
	if (os.path.exists(expandedpath)):
		print(bcolors.HEADER,"Profiles:",bcolors.ENDC)
		with open(expandedpath) as file:
			for line in file:
				if line.startswith('['):
					print(bcolors.BOLD,line[1:-2],bcolors.ENDC)
					profilelist.append([i,line[1:-2]])
					i += 1

if __name__ == '__main__':
	main()
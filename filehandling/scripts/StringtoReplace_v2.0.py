#

import os
import sys
import fileinput


def convertfile(folder):
	textToSearch1 = " I "
	textToSearch2 = " l "
	textToSearch3 = " ] "
	textToSearch4 = " [ "
	textToSearch5 = " E "
	textToSearch6 = " t "
	for file in os.listdir(folder):
		if file.endswith(".txt"):
			with fileinput.FileInput(os.path.join(folder,file), inplace=True, backup='.bak') as openfile:
				for line in openfile:
					if textToSearch1 in line:
						print(line.replace(textToSearch1, '\n'), end='')
					if textToSearch2 in line:
						print(line.replace(textToSearch2, '\n'), end='')
					if textToSearch3 in line:
						print(line.replace(textToSearch3, '\n'), end='')
					if textToSearch4 in line:
						print(line.replace(textToSearch4, '\n'), end='')
					if textToSearch5 in line:
						print(line.replace(textToSearch5, '\n'), end='')
					if textToSearch6 in line:
						print(line.replace(textToSearch6, '\n'), end='')

def main():
	folder = sys.argv[1]
	if os.path.exists(folder):
		convertfile(folder)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('')
		print('\033[1m' + '\nKeyboard Interruption..Calm Down')
		print('\033[1m' + '\nExiting !!!!\n')
		print('\033[0m')
		sys.exit()



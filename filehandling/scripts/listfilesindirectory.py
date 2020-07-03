import os
import sys
import fileinput


def convertfile(folder):
	textToSearch = " I "

	for file in os.listdir(folder):
		if file.endswith(".txt"):
			with fileinput.FileInput(os.path.join(folder,file), inplace=True, backup='.bak') as openfile:
				for line in openfile:
					print(line.replace(textToSearch, '\n'), end='')


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



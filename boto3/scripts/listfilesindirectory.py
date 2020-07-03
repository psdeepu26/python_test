import os
import sys


def convertfile(folder):
	for file in os.listdir(folder):
		if file.endswith(".txt"):
			print(os.path.join(folder,file))


def main():
	folder = sys.argv[1]
	if os.path.exists(folder):
		convertfile(folder)

if __name__ == '__main__':
	main()



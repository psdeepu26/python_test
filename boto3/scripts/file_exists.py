import sys
import os

print(os.path.exists(sys.argv[1]))
if (os.path.exists(sys.argv[1])):
	print("good")
else:
	print("File doesn't exist, Exiting the Script")
	sys.exit()

import argparse
parser = argparse.ArgumentParser(description="Used for login to the AWS instance")
parser.add_argument("-f", "--file", action="store", help="Provide the absolute path of the pem file")
args = parser.parse_args()
file = args.file

print(file)
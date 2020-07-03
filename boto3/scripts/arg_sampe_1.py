import argparse
parser = argparse.ArgumentParser(description="simple script")
parser.add_argument("-a",action="store_true",default=False)
parser.add_argument("-s","--square",help="square the number", type=int)
args = parser.parse_args()
print(args.square**2)
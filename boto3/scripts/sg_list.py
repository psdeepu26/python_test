#List all the Security groups in the account

import boto3

ec2 = boto3.resource('ec2')
SGs = ec2.security_groups.all()

for SG in SGs:
	print(SG.)

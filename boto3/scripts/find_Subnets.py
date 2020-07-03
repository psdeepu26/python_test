# This program is used to find a specific subnet group/s and its sunbet group id
# here in this am trying to find the sunbets which has 'PSD' name in it

import boto3

ec2 = boto3.resource('ec2')
subnets = ec2.subnets.all()


# Using the normal way
# Commenting the below part but this works
for subnet in subnets:
	for tag in subnet.tags:
		if tag['Key'] == "Name":
			if 'PSD' in tag['Value']:
				print(tag['Value'],subnet.subnet_id)

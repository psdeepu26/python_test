# This program is used to get all the Subnets groups 

import boto3

ec2 = boto3.resource('ec2')
subnets = ec2.subnets.all()

# Used List Comprehension to get the list
subnet_list = [tag['Value'] for subnet in subnets for tag in subnet.tags if tag['Key'] == "Name"]
print(subnet_list)


# Using the normal way
# Commenting the below part but this works
#for subnet in subnets:
#	for tag in subnet.tags:
#		if tag['Key'] == "Name":
#			print(tag['Value'])








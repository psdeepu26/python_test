# This program is to list all the EC2 instances in your account
import boto3

ec2 = boto3.resource('ec2')
instances = ec2.instances.all()
for instance in instances:
	print(instance.instance_id,instance.tags[0]['Value'],instance.subnet_id)

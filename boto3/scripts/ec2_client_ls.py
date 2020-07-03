import boto3

client = boto3.client('ec2')
responses = client.describe_instances()

for response in responses['Reservations']:
	for instance in response['Instances']:
		print(instance['InstanceId'])
		print(instance)
	
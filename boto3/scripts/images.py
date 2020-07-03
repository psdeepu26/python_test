import boto3

ec2 = boto3.resource('ec2')
images = ec2.images.all()

for image in images:
	print(image)
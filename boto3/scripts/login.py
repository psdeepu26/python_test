import boto3
import os
import subprocess



client = boto3.client('ec2')
responses = client.describe_instances()

PrivateIPs = []

for idx, response in enumerate(responses['Reservations'], start=1):
	print(idx, "\t",response['Instances'][0]['InstanceId'],"\t",response['Instances'][0]['PrivateIpAddress'],"\t",response['Instances'][0].get('PublicIpAddress',''))
	PrivateIPs.append(response['Instances'][0]['PrivateIpAddress'])

choice = input("Enter your Choice: ")
choice_instance = PrivateIPs[int(choice)-1]
command = 'ssh -i /Users/spatrayuni/Downloads/intuit_learning.pem ec2-user@'+choice_instance+' -o "proxycommand=ssh -W %h:%p -i /Users/spatrayuni/Downloads/intuit_learning.pem ec2-user@35.163.71.151"'
print(command)
os.system(command)
#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#process = subprocess.Popen(command)
#output, error = process.communicate()


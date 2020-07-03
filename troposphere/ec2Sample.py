from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2
import boto3

# Part 1: Using boto SDK to locate AMI Id

# Insert your access key, secret access key and region here
client = boto3.client('ec2',
                        aws_access_key_id='AKIAJQ5EOAMKOBO6XHEQ',
                        aws_secret_access_key='Ap6RJBZkTyfB0Qb2O/0eGg31BqtzURbTukgFrfAz',
                        region_name='us-west-2')

# Get a list of AMIs that are owned by you. 
# In case you want to list private images, filter based on ExecutableUsers instead of Owners
# e.g. ExecutableUsers=['your aws account number']
response = client.describe_images(Owners=['self'])
images = response['Images']


# Find the image that was recently created
imageDate = None
latestAMI = None
for image in images:
        if image['CreationDate'] > imageDate:
                imageDate=image['CreationDate']
                latestAMI = image['ImageId']

latestAMI = "ami-6f46da0f"


# Part 2: Using the AMI id to create a cloudformation template

template = Template()

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

# Replace security group ids & subnet id from the actual values from your AWS account
ec2_instance = template.add_resource(ec2.Instance(
    "Ec2Instance",
    ImageId=latestAMI,
    InstanceType="t2.micro",
    KeyName=Ref(keyname_param),
    SecurityGroupIds=["sg-0816ce73"],
    SubnetId="subnet-5e43f317"
))

template.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(ec2_instance),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicDnsName"),
    )
])

print(template.to_json())

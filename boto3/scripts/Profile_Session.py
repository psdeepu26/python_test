# Login into an Account get the daata, it wont set the session to Default

import boto3.session

learn = boto3.session.Session(profile_name='deepu_new')
#mmu = boto3.session.Session(profile_name='mmu')

print('Profile: ' + learn.profile_name)
ec2 = learn.client('ec2')
print(ec2.describe_instances())

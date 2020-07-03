'''
Version : v1.0
Problem Statement : To automate the Rollback process which is not possible with Slingshot account
How it works:
This script is used to Rollback ELB to old instances if any deployment fails
1. Get the list of ec2 instances attached to Blue ELB
2. From the input argument of (n-1) ASG, we will get the list of EC2 instances
3. Add the (n-1) ASG instances to BlueELB
4. Remove the (n) instances from BlueELB
5. Check the health of the instances
Script Input : Rollback.py
'''
import boto3
import argparse
import time
from boto3.exceptions import botocore
from texttable import Texttable

__ver__ = "1.0.0"

class bcolors:
    """Setting Text ForeGround Color"""
    BOLD = '\033[1m'
    HEADER = '\033[95m' + BOLD
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m' + BOLD
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    OK = BOLD + OKGREEN + u'\u2705' + "  "
    ERR = BOLD + FAIL + u"\u274C" + "  "
    WAIT = BOLD + OKBLUE + u'\u231b' + "  "
    HELP = OKBLUE
    BHELP = FAIL + BOLD
    BMSG = BOLD + OKBLUE
    DONE = BOLD + "Done " + u"\u2705"

def GetinstancesinASG(asg, client):
	ec2list = []
	#client = Profile_Session.client('autoscaling')
	response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
	for asg in response['AutoScalingGroups']:
		for instance in asg['Instances']:
			ec2list.append(instance['InstanceId'])
	return(ec2list,len(ec2list))

def GetinstancesinELB(elb, client):
	ec2list =[]
	#client = Profile_Session.client('elb')
	response = client.describe_load_balancers(LoadBalancerNames=[elb])
	for rep in response['LoadBalancerDescriptions']:
		for ec2 in rep['Instances']:
			ec2list.append(ec2['InstanceId'])
	return(ec2list,len(ec2list))

def register_oldasg(asg,elb,client):
	for ec2 in asg:
		try:
			response = client.register_instances_with_load_balancer(
	    		LoadBalancerName=elb,
	    		Instances=[
	        	{
	            	'InstanceId': ec2
	        	},
	    		]
			)
		except botocore.exceptions.ClientError as errObj:
			print(bcolors.ERR + str(errObj),bcolors.ENDC)
	ec2list = []
	for rep in response['Instances']:
		ec2list.append(rep['InstanceId'])
	return(ec2list,len(ec2list))

def deregister_oldasg(asg,elb,client):
	for ec2 in asg:
		try:
			response = client.deregister_instances_from_load_balancer(
	    		LoadBalancerName=elb,
	    		Instances=[
	        	{
	            	'InstanceId': ec2
	        	},
	    		]
			)
		except botocore.exceptions.ClientError as errObj:
			print(bcolors.ERR + str(errObj),bcolors.ENDC)
	ec2list = []
	for rep in response['Instances']:
		ec2list.append(rep['InstanceId'])
	return(ec2list,len(ec2list))

def elb_instance_health(elb,register_result, client, status):
	ec2list = []
	idx = 1
	count = 0
	if status == "before":
		for ec2 in register_result:
			response = client.describe_instance_health(
		    	LoadBalancerName=elb,
		    	Instances=[
		        	{
		            	'InstanceId': ec2
		        	},
		    	]
			)
			for rep in response['InstanceStates']:
				ec2list.append([idx, rep['InstanceId'], rep['State']])
				idx = idx + 1
		print(bcolors.OKBLUE,'Please find the Instances and their current healths in ELB - "{}"'.format(elb),bcolors.ENDC)
		t = Texttable()
		t.add_rows(ec2list)
		print(t.draw())
	elif status == "after":
		for ec2 in register_result:
			response = client.describe_instance_health(
		    	LoadBalancerName=elb,
		    	Instances=[
		        	{
		            	'InstanceId': ec2
		        	},
		    	]
			)
			for rep in response['InstanceStates']:
				ec2list.append([idx, rep['InstanceId'], rep['State']])
				if rep['State'] == "OutOfService":
					count = count + 1
				idx = idx + 1
		if count  == 0:
			print(bcolors.OKBLUE,'Please find the Instances and their current healths in ELB - "{}"'.format(elb),bcolors.ENDC)
			t = Texttable()
			t.add_rows(ec2list)
			print(t.draw())
		else:
			print(bcolors.WAIT,'None of the instances are healthy',bcolors.ENDC)
			print(bcolors.OKBLUE,'Please find the Instances and their current healths in ELB - "{}"'.format(elb),bcolors.ENDC)
			t = Texttable()
			t.add_rows(ec2list)
			print(t.draw())
			elb_instance_health(elb,register_result, client, status)


def description():
    '''
    Rollback to OLD Stack
    This script is used to Rollback the ELB to the old Stack
    '''

def main():
	parser = argparse.ArgumentParser(description=description.__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-o", "--oldasg", action="store", dest="old_asg", help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "Provide Old ASG Name" + bcolors.ENDC,required=True)
	parser.add_argument("-e", "--elb", action="store", dest="elb_env", help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "Provide ELB Name" + bcolors.ENDC,required=True)
	parser.add_argument("-p", "--profilename", action="store", dest="aws_profile", help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "Provide Profile Name" + bcolors.ENDC,required=True)
	parser.add_argument("-r", "--region", action="store", dest="aws_region", required=True, help=bcolors.BHELP + "[REQUIRED]:" + bcolors.HELP + "AWS Region" + bcolors.ENDC)
	args = vars(parser.parse_args())
	oldasg = args['old_asg']
	elb = args['elb_env']
	profilename = args['aws_profile']
	aws_region = args['aws_region']
	status = "before"

	print(bcolors.HEADER,'This Script will Rollback instances of ELB "{}"'.format(elb),'to old ASG "{}"'.format(oldasg),bcolors.ENDC)
	correct_aws_region = ['us-west-2', 'us-east-1']
	if aws_region not in correct_aws_region:
		print(bcolors.ERR,'Invalid AWS Region passed. Valid values are {}'.format(correct_aws_region),bcolors.ENDC)
		raise ValueError
	print(bcolors.OK,'Region "{}" Verfied'.format(aws_region),bcolors.ENDC)

	try :
		Profile_Session = boto3.session.Session(profile_name=profilename,region_name=aws_region)
	except botocore.exceptions.ProfileNotFound:
		print(bcolors.ERR,'Profile {} not found in ~/.aws/credentials.'.format(profilename),bcolors.ENDC)
		raise ValueError
	print(bcolors.OK,'Profile "{}" Verfied'.format(profilename),bcolors.ENDC)

	asg_client = Profile_Session.client('autoscaling')
	#asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[oldasg])

	elb_client = Profile_Session.client('elb')
	#elb_response = elb_client.describe_load_balancers(LoadBalancerNames=[elb])

	asg_ec2list, len_asg = GetinstancesinASG(oldasg,asg_client)
	if not asg_ec2list:
		print(bcolors.ERR,'Provided Autoscaling Group is either wrong or has no instances on it',bcolors.ENDC)
		raise ValueError
	else:
		print(bcolors.OK,'ASG "{}" Verfied'.format(oldasg),bcolors.ENDC)
		print(bcolors.OKBLUE,'Currently ASG - "{}" has {} instances- {}'.format(oldasg,len_asg,asg_ec2list),bcolors.ENDC)

	elb_ec2list, len_elb = GetinstancesinELB(elb,elb_client)
	if not elb_ec2list:
		print(bcolors.WARNING,'Currently ELB - "{}" doesn\'t have any Instances running on it'.format(elb),bcolors.ENDC)
	else:
		print(bcolors.OK,'ELB "{}" Verfied'.format(elb),bcolors.ENDC)
		print(bcolors.OKBLUE,'Currently ELB - "{}" has {} instances- {}'.format(elb,len_elb,elb_ec2list),bcolors.ENDC)
		elb_instance_health(elb,elb_ec2list,elb_client,status)

	if set(asg_ec2list) == set(elb_ec2list):
		print("\n")
		print(bcolors.DONE,' ASG - "{}" and ELB - "{}" have the same instance {}'.format(oldasg,elb,elb_ec2list),bcolors.ENDC)
		elb_instance_health(elb,elb_ec2list,elb_client,status)
		return

	register_result, len_register = register_oldasg(asg_ec2list,elb,elb_client)
	if len_register > len_elb:
		print()
		print(bcolors.OK,'Successfully added {} instances to ELB - "{}"'.format(asg_ec2list,elb),bcolors.ENDC)
		elb_instance_health(elb,register_result,elb_client,status)
		#print(bcolors.OKBLUE,'Currently ELB - "{}" has {} instances - {}'.format(elb,len_register,register_result),bcolors.ENDC)
	#print(bcolors.HEADER,'This Script will Rollback instances of "{}"'.format(elb),'to old Autoscaling Group "{}"'.format(oldasg),bcolors.ENDC)

	if elb_ec2list:
		deregister_result, len_deregister = deregister_oldasg(elb_ec2list,elb,elb_client)
	if len_deregister < len_register:
		print()
		status = "after"
		print(bcolors.OK,'Successfully removed old instances {} to ELB - "{}"'.format(elb_ec2list,elb),bcolors.ENDC)
		elb_instance_health(elb,deregister_result,elb_client,status)
		#print(bcolors.OKBLUE,'Currently ELB - "{}" has {} instances- {}'.format(elb,len_register,register_result),bcolors.ENDC)

	print("\n")
	print(bcolors.DONE,'Rollback Completed Successfully',bcolors.ENDC)


if __name__ == '__main__':
	start_time = time.time()
	try:
		main()
	except KeyboardInterrupt:
		print("")
		print(bcolors.ERR,'User Interruption received. Existing...',bcolors.ENDC)
	except botocore.exceptions.ClientError as errObj:
		print(bcolors.ERR + str(errObj),bcolors.ENDC)
	except ValueError:
		print(bcolors.ERR,"Invalid Value Types are passed.",bcolors.ENDC)
	except Exception as error:
		print(bcolors.ERR,'Caught this error: ',repr(error),bcolors.ENDC)
	print()
	print(bcolors.BOLD,"Total Script Execution Time: {0:.2f} seconds".format(time.time() - start_time),bcolors.ENDC)

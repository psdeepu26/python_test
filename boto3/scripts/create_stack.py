import boto3
client = boto3.client('cloudformation')
response = client.create_stack(
    StackName='InstanceSG',
    TemplateURL='https://s3-us-west-2.amazonaws.com/psd26/InstanceSecurityGroup.template',
    Parameters=[
        {
            'ParameterKey': 'VpcId',
            'ParameterValue': 'vpc-583f7f3f',
        },
        {
            'ParameterKey': 'BastionSG',
            'ParameterValue': 'sg-0816ce73',
        },
        {
            'ParameterKey': 'SGName',
            'ParameterValue': 'ngwi-qa-2',
        },
    ],
    TimeoutInMinutes=10,
    OnFailure='ROLLBACK',
)


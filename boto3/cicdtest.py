import boto3
import os
import sys
import uuid

s3_client = boto3.client('s3')
sns = boto3.client("sns")

topic_arn = "arn:aws:sns:us-west-2:393531488165:s3testsns"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)
        print("Downloading Starting")
        s3_client.download_file(bucket, key, download_path)
        #resize_image(download_path, upload_path)
        #s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)
        print("Image is downloaded")

        sns_message = f"Image is downloaded and it is from CICDTestDemo"

        response = sns.publish(TopicArn=topic_arn, Message = sns_message)

        print("SNS sent to email")

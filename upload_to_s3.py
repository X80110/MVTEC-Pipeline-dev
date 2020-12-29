import logging
import boto3
from botocore.exceptions import ClientError
from config import bucket, folder, region
from notify import send_email, email_body, recipients



# Upload to S3, bucket details are set in config.py
def upload_to_s3(body, filename):
    s3_client = boto3.client('s3')
    try:
        target = "%s/%s" % (folder, filename)
        s3_client.put_object(Body=body, Bucket=bucket, Key=target)
        log = "File uploaded: https://%s.s3-%s.amazonaws.com/%s" % (bucket, region, target)
        logging.info(log)
        send_email('xbollo@gmail.com','Files updated successfully to S3',email_body(log))
    
    except ClientError as e:
        log = "Error occurred: %s" % e
        logging.error(log)
        send_email(recipients,'Something failed updating files in S3',email_body(log))
        return False
    return True



# Trying to update S3 bucket policy to set up public access to files - Not enough permissions set to our user
# ---------------------------
# import json
# s3 = boto3.client('s3')
# bucket_policy = {
# "Version": "2012-10-17",
# "Statement": [
#     {
#         "Sid": "AddPerm",
#         "Effect": "Allow",
#         "Principal": "*",
#         "Action": [
#             "s3:PutObject",
#             "s3:PutObjectAcl",
#             "s3:GetObject"
#         ],
#         "Resource": "arn:aws:s3:::%s/*" % bucket
#     }]
# }   
# # Convert the policy to a JSON string
# bucket_policy = json.dumps(bucket_policy)
#
# # Set the new policy on the given bucket
# s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
#
# # Check bucket policy
# result = s3.get_bucket_policy(Bucket=bucket)
# print(result)
# 
# ---------------------------

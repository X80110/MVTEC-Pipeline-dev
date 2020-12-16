import logging
import boto3
from botocore.exceptions import ClientError
from config import bucket, folder, region

def upload_to_s3(body, filename):
    s3_client = boto3.client('s3')
    try:
        target = "%s/%s" % (folder, filename)
        s3_client.put_object(Body=body, Bucket=bucket, Key=target)
        logging.info("Uploaded: https://%s.s3-%s.amazonaws.com/%s" % (bucket, region, target))
    except ClientError as e:
        logging.error(e)
        return False
    return True

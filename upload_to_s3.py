import logging
import boto3
from botocore.exceptions import ClientError
from config import bucket, folder, region
from notify import send_email, recipients
from check_uploaded_file import data_overview_mail


# Upload to S3, bucket details are set in config.py
def upload_to_s3(body, filename):
    s3_client = boto3.client('s3')
    try:
        target = "%s/%s" % (folder, filename)
        s3_client.put_object(Body=body, Bucket=bucket, Key=target, ACL='public-read')
        fileurl = "https://%s.s3-%s.amazonaws.com/%s" % (bucket, region, target)
        log = "File has been updated: %s" % fileurl
        logging.info(log)
        send_email('xbollo@gmail.com','Files updated successfully to S3',log)
        data_overview_mail(fileurl)
    
    except ClientError as e:
        log = "Error occurred: %s" % e
        logging.error(log)
        send_email(recipients,'Error while updating files in S3',log)
        return False
    return True
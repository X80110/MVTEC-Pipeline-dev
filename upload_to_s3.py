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
        notify_upload = '\n ✔ Files updated successfully to S3\n'
        print(notify_upload)
        #logging.info(log)
        
    except ClientError as e:
        log = "Error occurred: %s" % e
        logging.error(log)
        x_notify_upload = '\n ☠️ Error while updating files in S3\n'
        print(x_notify_upload)
        return False
    return True
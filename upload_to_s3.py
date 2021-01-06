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
        notify_upload = '✓ 3. Files updated successfully to S3'
        
    except ClientError as e:
        log = "Error occurred: %s" % e
        logging.error(log)
        x_notify_upload = '☠️ 3.Error while updating files in S3'
        print(x_notify_upload)
        return False
    return True, x_notify_upload, notify_upload
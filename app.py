import logging, time
import boto3
import datetime
from botocore.exceptions import ClientError
import config
import requests
import json
import notify

# define source, output filename and folder  
URL = "https://coviddata.github.io/coviddata/v1/countries/stats.json"
file = 'covid_data.json'
folder = 'project'

# define how to put object using s3 library boto3
def dataupload(file,content):
    s3 = boto3.client('s3')
    target = "%s/%s" % (folder, file)
    try: 
        s3.put_object(
            Body=str(json.dumps(content)),
            Bucket='snxmvtec-test',
            Key=target)
        logging.info("🙌 It looks good!")
        logging.info("⏳ Please wait a moment for the validation from server...")
    except ClientError as e:
        logging.error(e)
        return False
    return True

logging.info("Starting app...")

# Run the process 
while True:
    # Get the data from source
    r = requests.get(URL)
    content = r.json()

    # Upload to s3
    dataupload(file,content)
    
    # Validate response status_code: 200 from s3
    validate = "https://mvtec-dataeng-assignment7.s3-eu-west-1.amazonaws.com/xbollo/%s" % (file)
    v = requests.get(validate)
    now = datetime.datetime.now()
    if v.status_code == 200:
        logging.info('✅ That is nice! S3 Server sent your -deserved- status code: 200')
        logging.info('🤘 File updated on %s' % now.strftime("%Y-%m-%d %H:%M"))
        logging.info('⬇️ File should be accessible here: %s' % validate)
    else:
        logging.info('☠️ The server hates you' % v.status_code)
    
    # Restart loop after 1 day = 60s*60min*24h = 86400s
    time.sleep(86400)

# log for the server
if __name__ == "__main__":
    while True:
        logging.info("👌 App is running fine")
        time.sleep(60)

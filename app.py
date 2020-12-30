import subprocess
import os
import logging, time
import config
from upload_to_s3 import upload_to_s3
from notify import send_email, recipients

# set local path
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

try:    
    # run rscripts on the server runtime
    result = subprocess.run(["Rscript","Rscripts/xavier_dataprep.R"], capture_output=True)
    output = result.stdout.decode()
    if 'error' in output: 
        print("Error running the scripts, email have been sent")
        print("Details: %s" % output)
        send_email(recipients,'Scripts not found' ,output)
    else:
        # uplodad output to S3
        upload_to_s3(body=output, filename="data-test.csv")
except Exception: 
    log = result.stderr.decode()
    print(log)
    print("Scripts couldn't be read properly")
    send_email(recipients,'Heroku scripts failed to run' ,log)
    exit(1)





# df = pd.read_csv('tmp/merged_data.csv')
# print(df)

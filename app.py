import subprocess
import os
import logging, time
import config
from upload_to_s3 import upload_to_s3
from notify import send_email, recipients
from scraper import usd_twd_scrap

# set local path
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

####
# Main workflow steps:
#   - 1. Scrape updated USD-TWD exchange 
#       - a. Fetch data from previous days from S3
#       - b. Input scraped data
#       - c. Update news values into S3 file
#   - 2. Run Rscripts with the statistical models, 2 external inputs:
#       - a. ourworldindata.org
#       - b. Exchange values scraped (step 1)
#       - c. Capture the output and upload to S3 as a file
#   - 3. Handling status and notifications about the process
#       - a. (1) Url availability *(Console)*
#       - b. (1) Update file into S3 *(Email[x] - Console)   // [x] = only if pipeline is unable to move forward*
#       - c. (2) Read, process R model and capture output *(Console)*
#       - d. (2) Read file and process *(Email[x] - Console)*
#       - e. (2) Upload to S3 *(Email - Console)*
#       - f. (3) Report pipeline status *(Email - Console)*
####

try:    
# 1. Scrape updated USD-TWD exchange
    usd_twd_scrap()
    
    # Update values to S3
    # upload_to_s3(body=combined, filename="currency_output.csv")
    # integrated into the function usd_twd_scrap

    time.sleep(15)  # slow down the code to ensure data streams from cloud delay and risk miss steps
    
    # notify variables are collected and then pushed to the body
    notify_exchange = "✔ 1.USD-TWD exchanges has been update to S3"
    print(notify_exchange)

# 2. Run Rscripts with the statistical models, 2 external inputs:
    result = subprocess.run(["Rscript","Rscripts/spe_dataprep4model.R"], capture_output=True)
    output = result.stdout.decode()

    # some warnings in R are interpreted as Exception making the code skip the remaining steps
    # capture and notify if errors are logged into Rscript output // TODO Check logic, is a matter of time that desired output contains the string 'error' to mislead the step
    if 'error' in output: 
        x_notify_rscripts = '☠️ 2. The R scripts failed to run'
        print(x_notify_rscripts, output)
        print("Details: %s" % output)
    else: 
        notify_rscripts =  "✔ 1.USD-TWD exchanges has been updated to S3"
    
    # uplodad output to S3
    upload_to_s3(body=output, filename="usdtwd_prediction.csv")
        # Notifications are handled directly by the function
    
# 3. Main process failure notification, code shoud never reach here!
except Exception: 
    log = result.stderr.decode()
    print(log)
    x_notify_failure = "☠️ 3. Pipeline failed to run"
    print(x_notify_failure)

notify_success = "✔ 3. Scripts ran successfuly"
print(notify_success)
# emailbody = [
#     notify_exchange,
#     x_notify_exchange,
#     notify_upload,
#     x_notify_upload,
#     notify_rscripts,
#     x_notify_rscripts,
#     notify_success,
#     notify_failure,
#     ]
# # data_overview_mail(fileurl)
# send_email('xbollo@gmail.com',*emailbody,log)
exit(1)


# TODO add data overview table
# df = pd.read_csv('tmp/merged_data.csv')
# print(df)

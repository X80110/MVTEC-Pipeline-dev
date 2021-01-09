import subprocess
import os
import logging, time
from datetime import date
import config
from notify import send_email, recipients, to_report
from scraper import usd_twd_scrap
from upload_to_s3 import upload_to_s3
from overview import overview

# set local path
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

####
# Main workflow steps:
#   - 1. Scrape updated USD-TWD exchange 
#       - a. Fetch data from previous days from S3
#       - b. Scrap currency values on invest.com
#       - c. Update values into S3 file currency_output.csv
#   - 2. Run Rscripts, the inputs required:
#       - a. currency_output.csv
#       - b. ourworldindata.org 
#   - 3. Update R results as usdtwd_prediction.csv and dailystats.csv
#   - 4. Send email with report and overview of the values in each file
####
logging.info("Starting app...")
try:       
    # 1. Scrape updated USD-TWD exchange
    try:
        usd_twd_scrap()
        # Update values to S3
        # upload_to_s3(body=combined, filename="currency_output.csv")
        # integrated into the function usd_twd_scrap
        time.sleep(15)  # slow down the code to ensure data streams from cloud delay and risk miss steps
        
        # notify variables are collected and then pushed to the body
        
        # to_report.append(notify_exchange)
        # print(notify_exchange)

    except Exception:
        x_notify_exchange = '☠️ Could not update currency values'
        to_report.append(x_notify_exchange)
        print('x_notify_exchange')

    try:
    # 2.1 Run Rscripts with the statistical models
        result = subprocess.run(["Rscript","Rscripts/dataprep4model.R"], capture_output=True)
        output = result.stdout.decode()

        notify_rscripts =  "✔ Model scripts ran successfuly"
        to_report.append(notify_rscripts)
        upload_to_s3(body=output, filename="usdtwd_prediction.csv")

    except Exception: 
        log = result.stderr.decode()
        x_notify_rscripts = '☠️ The R scripts failed to run'
        to_report.append(x_notify_rscripts)
        print(x_notify_rscripts, log)   


# 2.2 Process mainly stats (not critical if failed)
    result2 = subprocess.run(["Rscript","Rscripts/dataprep.R"], capture_output=True)
    output2 = result2.stdout.decode()
    upload_to_s3(body=output2, filename="dailystats.csv")
    
# 3. Main process failure notification, code shoud never reach here!
except Exception: 
    x_notify_failure = "☠️ Pipeline failed to run"
    to_report.append(x_notify_failure)
    print(x_notify_failure)

# Build report ----------------------
to_report.append("Pipeline status:")

# Summary covid table
table1 = overview()[0][0]
# Currency table
table2 = overview()[0][1]
# Prediction table
table3 = overview()[0][2]
# Overview urls
to_report.append(overview()[1])

# Send email
subject = '[MVTEC-pipeline] Report for %s' % (date.today().strftime('%B-%d'))
report = '\n'.join(to_report)
try:
    send_email(recipients, subject,report,table1,table2,table3)
except Exception:
    print("Email delivery failed")
end = '[MVTEC-pipeline] End of the script, server set to sleep until' % (date.today().strftime('%B-%d')+1)
logging.info(end)
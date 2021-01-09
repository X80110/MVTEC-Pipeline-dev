import smtplib
import ssl 
import os 
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Get emails from environment 
emails  = os.environ.get('recipients')
recipients = emails.split(',')

# Object to collect pipeline messages and append to the body at the end of the flow
to_report = []

# notifications = {
#     # currency
#     # "notify_exchange" : "\n ✔ 1.USD-TWD exchanges has been updated to S3\n",
#     # "x_notify_exchange" : "\n ☠️ 1. The file could not be uploaded to S3\n",
#     "x_notify_source_url" : "\n Data source is not responding. We will use archive csv.\n", 
#     # scripts
#     "notify_rscripts" :  "✔ 2. The R scripts run successfuly",
#     "x_notify_rscripts" : '☠️ 2. The R scripts failed to run',
#     # file upload
#     "notify_upload" : '\n ✔ Files updated successfully to S3\n File: %s\n Url: %s\n' % {filename, fileurl},
#     "x_notify_upload" : '\n ☠️ Error while updating files in S3\n, ',
#     # pipeliine failure
#     "x_notify_failure" : "\n☠️ 3. ERROR! Pipeline failed to run\n",
# }
# notifications['x_notify_failure']


# create the connection
def send_email(to_addr, subject, body, table1=None, table2=None,table3=None): #`None` makes the variable not mandatory and as the default
    found_credentials = EMAIL_USERNAME and EMAIL_PASSWORD
    if not found_credentials:
        print("Can't find credenetials")
        exit(1)

    #message = f'Subject: {subject}\n\n {body}'
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = EMAIL_USERNAME
    message['To'] = ', '.join(to_addr)  # push it as string
    body_content = str(body) # convert to string to avoid encoding issues in R stdout
    if table1 == None: 
        message.attach(MIMEText(body_content,"plain"))
    else:
        message.attach(MIMEText(body_content,"plain"))
        message.attach(MIMEText(table1,"html"))
        message.attach(MIMEText(table2,"html"))
        message.attach(MIMEText(table3,"html"))
    msg_body = message.as_string()
    #----
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context= context) as server: 
        # login / authenticate
        server.login(EMAIL_USERNAME,EMAIL_PASSWORD)
        # send the email
        server.sendmail(EMAIL_USERNAME,to_addr,msg_body)
        print("\nEmail sent successfully")

#*Usage*
#try:
#    send_email(recipients,subject, body)
#except Exception:
#    print("Email delivery failed")

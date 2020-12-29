import smtplib
import ssl 
import os 
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# The smtp 
# message = """ Subject: This is a test
#
# this is a body"""

recipients  = ['xbollo@gmail.com','spepe.chen@gmail.com','nuria.altimir@gmail.com']
# simplify email body creation
def email_body(log,*table):
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M")
    print("Updated on %s \n %s \n\n Last values %s" % (time, log, table)) 

# create the connection
def send_email(to_addr, subject, body):
    found_credentials = EMAIL_USERNAME and EMAIL_PASSWORD
    if not found_credentials:
        print("Can't find credenetials")
        exit(1)

    #message = f'Subject: {subject}\n\n {body}'
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = EMAIL_USERNAME
    message['To'] = to_addr

    body_content = body
    message.attach(MIMEText(body_content))
    msg_body = message.as_string()
    #----
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context= context) as server: 
        # login / authenticate
        server.login(EMAIL_USERNAME,EMAIL_PASSWORD)
        # send the email
        server.sendmail(EMAIL_USERNAME,to_addr,msg_body)
        print("Email sent successfully")


#try:
#    send_email(recipients,subject, body)
#except Exception:
#    print("Email delivery failed")

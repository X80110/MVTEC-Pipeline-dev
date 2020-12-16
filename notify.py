import smtplib
import ssl 
import os 


EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

print(EMAIL_USERNAME)
# The smtp 
# message = """ Subject: This is a test
#
# this is a body"""

recipients = ['xbollo@gmail.com','melondulzon@gmail.com']
subject = 'You rock!'

body = 'Code ran all the way through!'

# create the connection
def send_email(to_addr, subject, body):
    found_credentials = EMAIL_USERNAME and EMAIL_PASSWORD
    if not found_credentials:
        print("Can't find credenetials")
        exit(1)

    message3 = f'Subject: {subject}\n\n {body}'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context= context) as server: 
        # login / authenticate
        server.login(EMAIL_USERNAME,EMAIL_PASSWORD)
        # send the email
        server.sendmail(EMAIL_USERNAME,to_addr,message3)
        print("Email sent successfully")
try:
    send_email(recipients,subject, body)
except Exception:
    print("Email delivery failed")

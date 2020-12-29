import requests
import pandas as pd
from datetime import date, timedelta
from pretty_html_table import build_table

from notify import send_email

URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
#r = requests.get(URL)
df = pd.read_csv(URL)
yesterday = date.today() - timedelta(days=2)
df = df[(df['date']==yesterday.strftime("%Y-%m-%d"))].sort_values(by='total_deaths', ascending=False).head(15)
pd.set_option('display.float_format','{:.0f}'.format)
day_before_data = df[['location','new_cases','new_deaths','total_cases','total_deaths']].round(0)


send_email('xbollo@gmail.com','test',day_before_data.as_string())



# while True:
#     # Get the data from source
#     r = requests.get(URL)
#     content = r.json()

#     # Upload to s3
#     dataupload(file,content)
    
#     # Validate response status_code: 200 from s3
#     validate = "https://mvtec-dataeng-assignment7.s3-eu-west-1.amazonaws.com/xbollo/%s" % (file)
#     v = requests.get(validate)
#     now = datetime.datetime.now()
#     if v.status_code == 200:
#         logging.info('✅ That is nice! S3 Server sent your -deserved- status code: 200')
#         logging.info('🤘 File updated on %s' % now.strftime("%Y-%m-%d %H:%M"))
#         logging.info('⬇️ File should be accessible here: %s' % validate)
#     else:
#         logging.info('☠️ The server hates you' % v.status_code)
    
#     # Restart loop after 1 day = 60s*60min*24h = 86400s
#     time.sleep(86400)
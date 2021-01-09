import requests
import pandas as pd
import os
import config
from io import StringIO
from upload_to_s3 import upload_to_s3
from notify import to_report

# scraping currency table 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
url = 'https://www.investing.com/currencies/usd-twd-historical-data'
previous_values = "https://mvtec-group3.s3-eu-west-1.amazonaws.com/project/currency_output.csv"
response = requests.get(url, headers=headers)

# Uncomment to run the the script locally 
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

def usd_twd_scrap():
    if response.status_code == 200:
    
        print(response)
        dfs = pd.read_html(response.text)
        df = dfs[0]
        # read the historical file
        currency_df = pd.read_csv(previous_values)
        
        # updating new date's rate
        combined = pd.concat([df, currency_df])
        combined['Date'] = pd.to_datetime(combined['Date'])
        combined = combined.drop_duplicates(subset='Date', keep="first")
        
        # manage csv format 
        output = StringIO()
        combined.to_csv(output)
        
        # upload to S3
        upload_to_s3(body=output.getvalue(), filename="currency_output.csv")
        # combined.to_csv('currency_output.csv', index=False)
              
        # else:
        #     x_notify_exchange = "\n ☠️ 1. The file could not be uploaded to S3\n"
        #     to_report.append(x_notify_exchange)
        #     print(x_notify_exchange)

    else: 
        x_notify_source_url = "\n Currency data source is not responding. We will use archive csv.\n", 
        to_report.append(x_notify_source_url)
        print(x_notify_source_url)


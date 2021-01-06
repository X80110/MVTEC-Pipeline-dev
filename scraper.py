import requests
import pandas as pd
import os
import config
from upload_to_s3 import upload_to_s3
from io import StringIO

# scraping currency table 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
url = 'https://www.investing.com/currencies/usd-twd-historical-data'
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
        currency_df = pd.read_csv('currency_output.csv')
        # updating new date's rate
        combined = pd.concat([df, currency_df])
        combined['Date'] = pd.to_datetime(combined['Date'])
        combined = combined.drop_duplicates(subset='Date', keep="first")
        # manage csv format to pass into S3
        output = StringIO()
        push_to_S3 = combined.to_csv(output)
        print(push_to_S3)
        print(combined)
        # combined.to_csv('currency_output.csv', index=False)

        upload_to_s3(body=push_to_S3, filename="currency_output.csv")
        notify_exchange = "✔ 1.USD-TWD exchanges has been update to S3"
        print(notify_exchange)
    else: 
        x_notify_exchange = "Data source is not responding. We will use archive csv."
        print(x_notify_exchange)
    
    return notify_exchange, x_notify_exchange






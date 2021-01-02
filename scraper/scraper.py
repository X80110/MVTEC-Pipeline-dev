import requests
import pandas as pd
from datetime import datetime
import pytz
import glob

# scraping currency table 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
url = 'https://www.investing.com/currencies/usd-twd-historical-data'
response = requests.get(url, headers=headers)

dfs = pd.read_html(response.text)
df = dfs[0]

# getting currency stored previously
for name in glob.glob('*[0-9].*'): #get filenames contain digit
    currency_filename = name
currency_df = pd.read_csv(currency_filename)

# updating
combined = pd.concat([df, currency_df])
combined['Date'] = pd.to_datetime(combined['Date'])
combined = combined.drop_duplicates(subset='Date', keep="first")

# save it with timestampe of date
tz_md = pytz.timezone('Europe/Madrid') 
date_str = datetime.now(tz_md).strftime("%Y%m%d")
print("Madrid date now:", date_str)

combined.to_csv('output' + date_str + '.csv', index=False)

print("updated currency table successfully")


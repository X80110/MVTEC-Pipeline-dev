import requests
import pandas as pd

# scraping currency table 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
url = 'https://www.investing.com/currencies/usd-twd-historical-data'
response = requests.get(url, headers=headers)

dfs = pd.read_html(response.text)
df = dfs[0]

# read the historical file
currency_df = pd.read_csv('currency_output.csv')

# updating new date's rate
combined = pd.concat([df, currency_df])
combined['Date'] = pd.to_datetime(combined['Date'])
combined = combined.drop_duplicates(subset='Date', keep="first")

combined.to_csv('currency_output.csv', index=False)
print("updated currency table successfully")

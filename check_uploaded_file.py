import pandas as pd
from datetime import date, timedelta
from pretty_html_table import build_table

from notify import send_email, recipients

# URL = 'https://mvtec-group3.s3-eu-west-1.amazonaws.com/project/data-test.csv'

def data_overview_mail(URL):
    # Create summary table ---
    df = pd.read_csv(URL)
    yesterday = date.today() - timedelta(days=2) # most recent set to 2 previous days from today to ensure values. 
    df = df[(df['date']==yesterday.strftime("%Y-%m-%d"))].sort_values(by='total_deaths', ascending=False).head(12)
    pd.set_option('display.float_format','{:.0f}'.format)
    day_before_data = df[['location','new_cases','new_deaths','total_cases','total_deaths']].round(0)
    date_output = yesterday.strftime("%Y-%m-%d")
    # Using pretty_html_table library to ease conversion from pandas to html table
    table = build_table(day_before_data, 'blue_light',font_family='Proxima Nova',font_size='small')
    # Table caption
    log = "Most recent data from date: %s \nDownload the output: \n%s" % (date_output, URL)
    print(log) 
    send_email(recipients,'Files has been updated to S3 successfuly',log,table)
    




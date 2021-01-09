import os
import pandas as pd
from datetime import date, timedelta
from pretty_html_table import build_table
from notify import send_email, recipients, to_report

this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

URL = 'https://mvtec-group3.s3-eu-west-1.amazonaws.com/project/'

# TODO: Add conditionals to process other content in files.



def overview():
    # Create summary ---
    URLstats = URL+'dailystats.csv'
    URLcurr = URL+'currency_output.csv'
    URLpred = URL+'usdtwd_prediction.csv'

    # Table daily stats usdtwd_prediction
    df = pd.read_csv(URLstats)
    yesterday = date.today() - timedelta(days=2) # most recent set to 2 previous days from today to ensure values. 
    pd.set_option('display.float_format','{:.0f}'.format)
    df = df[(df['date']==yesterday.strftime("%Y-%m-%d"))].sort_values(by='total_deaths', ascending=False).head(7)
    day_before_data = df[['location','new_cases','new_deaths','total_cases','total_deaths']].round(0)

    # Using pretty_html_table library to ease conversion from pandas to html table
    table1 = build_table(day_before_data, 'blue_light',font_family='Proxima Nova',font_size='small')

    # Table currency
    dfc = pd.read_csv(URLcurr).head(7).iloc[:, 1:7]
    table2 = build_table(dfc, 'blue_light',font_family='Proxima Nova',font_size='small')

    # Table prediction
    dft = pd.read_csv(URLpred).head(7)
    table3 = build_table(dft, 'blue_light',font_family='Proxima Nova',font_size='small')

    tables = [table1, table2, table3]
    date_output = date.today().strftime('%B %d')
    notify_details = "There's a preview of the data updated to S3 on %s \n Datasets are available here:\n - Main covid stats: %s\n - USD/TWD currency values: %s\n - Caculated values for the prediction %s" % (date_output, URLstats, URLcurr, URLpred)
    
    return (tables, notify_details)

    
        



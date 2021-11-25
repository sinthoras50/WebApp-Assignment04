import json
from pandas.core.frame import DataFrame
import pandas as pd
import urllib.request
import os
from datetime import datetime

API_KEY = 'AIzaSyDIBpTtapF9SmOzv8BcBGmITS41B1u-8Yc'

def load(url: str) -> DataFrame:
    error = 'None'
    
    df_results = pd.DataFrame(columns=
            ['datetime',
            'url',
            'HTTP_ERROR',
            'Overall_Category',
            'Largest_Contentful_Paint',
            'First_Input_Delay',
            'Cumulative_Layout_Shift',
            'First_Contentful_Paint',
            'Time_to_Interactive',
            'Total_Blocking_Time',
            'Speed_Index',
            'Dom_Size'])  
            
    # URL
    df_results.loc[0, 'url'] = url
    df_results.loc[0, 'datetime'] = datetime.now()

    try:
        result = urllib.request.urlopen(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}/&strategy=desktop&key={API_KEY}').read().decode('UTF-8')
        result_json = json.loads(result)

        # Overall Category
        df_results.loc[0, 'Overall_Category'] =\
            result_json['loadingExperience']['overall_category']   

        # Largest Contentful Paint    
        df_results.loc[0, 'Largest_Contentful_Paint'] =\
            result_json['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']

        # First Input Delay 
        fid = result_json['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']
        df_results.loc[0, 'First_Input_Delay'] = fid['percentile']

        # Cumulative Layout Shift    
        df_results.loc[0, 'Cumulative_Layout_Shift'] =\
        result_json['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']

        # First Contentful Paint 
        df_results.loc[0, 'First_Contentful_Paint'] =\
        result_json['lighthouseResult']['audits']['first-contentful-paint']['displayValue']

        # Time to Interactive  
        df_results.loc[0, 'Time_to_Interactive'] =\
        result_json['lighthouseResult']['audits']['interactive']['displayValue']

        # Total Blocking Time   
        df_results.loc[0, 'Total_Blocking_Time'] =\
        result_json['lighthouseResult']['audits']['total-blocking-time']['displayValue']

        # Dom Size
        df_results.loc[0, 'Dom_Size'] =\
        result_json['lighthouseResult']['audits']['dom-size']['displayValue']

        # Speed Index
        df_results.loc[0, 'Speed_Index'] =\
        result_json['lighthouseResult']['audits']['speed-index']['displayValue']
    except Exception as err:
        error = err

    # Error Logging
    df_results.loc[0, 'HTTP_ERROR'] = error

    return df_results

def write_csv(output: str, df: DataFrame, mode: str) -> None: 
    df.to_csv(output, index=False, header=(mode=='w'), mode=mode, encoding='latin-1')


if __name__ == '__main__':
    # write_csv('output1.csv', load('https://www.alza.sk/'), 'a' if os.path.isfile('output1.csv') else 'w')
    # write_csv('output2.csv', load('https://www.alza.sk/ako-nakupit-art13603.htm'), 'a' if os.path.isfile('output2.csv') else 'w')

    write_csv('amazon.csv', load('https://www.amazon.co.uk/'), 'a' if os.path.isfile('amazon.csv') else 'w')
    write_csv('google.csv', load('https://www.google.com/'), 'a' if os.path.isfile('google.csv') else 'w')
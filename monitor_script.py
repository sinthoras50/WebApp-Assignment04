import json
from pandas.core.frame import DataFrame
import pandas as pd
import urllib
import os
from datetime import datetime

# API request url
def load(url: str) -> DataFrame:
    error = 'None'
    
    # Create dataframe to store responses
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
            'Speed_Index'])  
            
    # URLs
    df_results.loc[0, 'url'] = url
    df_results.loc[0, 'datetime'] = datetime.now()

    try:
        result = urllib.request.urlopen(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}/&strategy=desktop').read().decode('UTF-8')
        result_json = json.loads(result)

        # Overall Category
        df_results.loc[0, 'Overall_Category'] =\
            result_json['loadingExperience']['overall_category']   

        # Core Web Vitals       

        # Largest Contentful Paint    
        df_results.loc[0, 'Largest_Contentful_Paint'] =\
            result_json['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']

        # First Input Delay 
        fid = result_json['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']
        df_results.loc[0, 'First_Input_Delay'] = fid['percentile']

        # Cumulative Layout Shift    
        df_results.loc[0, 'Cumulative_Layout_Shift'] =\
        result_json['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']

        # Additional Loading Metrics 

        # First Contentful Paint 
        df_results.loc[0, 'First_Contentful_Paint'] =\
        result_json['lighthouseResult']['audits']['first-contentful-paint']['displayValue']

        # Additional Interactivity Metrics 

        # Time to Interactive  
        df_results.loc[0, 'Time_to_Interactive'] =\
        result_json['lighthouseResult']['audits']['interactive']['displayValue']

        # Total Blocking Time   
        df_results.loc[0, 'Total_Blocking_Time'] =\
        result_json['lighthouseResult']['audits']['total-blocking-time']['displayValue']

        # Speed Index
        df_results.loc[0, 'Speed_Index'] =\
        result_json['lighthouseResult']['audits']['speed-index']['displayValue']

    except Exception as err:
        error = err


    # Error Logging
    df_results.loc[0, 'HTTP_ERROR'] = error

    return df_results

def write_csv(df: DataFrame, mode: str) -> None: 
    df.to_csv('output.csv', index=False, header=(mode=='w'), mode=mode, encoding='latin-1')


if __name__ == '__main__':
    write_csv(load('https://fmph.uniba.sk//'), 'a' if os.path.isfile('output.csv') else 'w')


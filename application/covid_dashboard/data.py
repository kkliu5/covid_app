"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
import requests


def create_dataframe():
    """Create Pandas DataFrame from JSON request"""
    data = requests.get('https://api.covidtracking.com/v1/us/daily.json').json()
    df = pd.DataFrame.from_dict(data)
    
    # Setting date column to date format
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # Dropping irrelvant/depreciated coulmns
    df = df.drop(columns=['dateChecked', 'lastModified', 'posNeg', 'total', 'hospitalized', 'recovered'])
    
    # Fixing a few rows that have the wrong values
    # Total test results does not show correct values when there are positive test cases
    # Therefore I increase the total test results to match the number of cases
    # This only effected 4 dates
    fix_1_19_20 = len(df.index) - 7
    fix_1_19_20 = len(df.index) - 8
    fix_1_19_20 = len(df.index) - 9
    fix_1_19_20 = len(df.index) - 10
    
    df.at[fix_1_19_20, 'totalTestResults'] = 1
    df.at[fix_1_19_20, 'totalTestResults'] = 1
    df.at[fix_1_19_20, 'totalTestResults'] = 2
    df.at[fix_1_19_20, 'totalTestResults'] = 2
    
    # Calculated columns
    # Rolling averages
    df['7d_ra_pos_in'] = df['positiveIncrease'].rolling(7).mean()
    df['30d_ra_pos_in'] = df['positiveIncrease'].rolling(30).mean()
    df['7d_ra_neg_in'] = df['negativeIncrease'].rolling(7).mean()
    df['30d_ra_neg_in'] = df['negativeIncrease'].rolling(30).mean()
    df['7d_ra_tot_res_in'] = df['totalTestResultsIncrease'].rolling(7).mean()
    df['30d_ra_tot_res_in'] = df['totalTestResultsIncrease'].rolling(30).mean()
    df['7d_ra_hos_in'] = df['hospitalizedIncrease'].rolling(7).mean()
    df['30d_ra_hos_in'] = df['hospitalizedIncrease'].rolling(30).mean()
    df['7d_ra_dth_in'] = df['deathIncrease'].rolling(7).mean()
    df['30d_ra_dth_in'] = df['deathIncrease'].rolling(30).mean()
    
    # Creating calulated columns Rates
    df['positive_rate'] = df['positive']/df['totalTestResults']
    df['negative_rate'] = df['negative']/df['totalTestResults']
    df['pending_rate'] = df['pending']/df['totalTestResults']
    df['hospitalized_rate'] = df['hospitalizedCumulative']/df['positive']
    df['ICU_rate'] = df['inIcuCumulative']/df['positive']
    df['ventilator_rate'] = df['onVentilatorCumulative']/df['positive']
    df['death_rate'] = df['death']/df['positive']
    df['hos_ICU_rate'] = df['inIcuCumulative']/df['hospitalizedCumulative']
    df['hos_ventilator_rate'] = df['onVentilatorCumulative']/df['hospitalizedCumulative']
    
    return df

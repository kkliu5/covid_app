"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from sodapy import Socrata

"""Calling data from CDC Source using Socrata"""
def call_client():
    # Authenticated client:
    client = Socrata("data.cdc.gov",
                     app_token="PRIVATE",
                     username="PRIVATE",
                     password="PRIVATE")

def create_case_death_df():
    """Data Pulls"""
    # Case & Death Data ~20s
    results = client.get_all("9mfq-cb36")
    df_case_death = pd.DataFrame.from_records(results)
    
    """Data Processing & Formatting"""
    # Case & Death Data
    # Changing data types
    df_case_death['submission_date'] = df_case_death['submission_date'].astype('datetime64')
    df_case_death['state'] = df_case_death['state'].astype('string')
    df_case_death['tot_cases'] = df_case_death['tot_cases'].astype('float')
    df_case_death['conf_cases'] = df_case_death['conf_cases'].astype('float')
    df_case_death['prob_cases'] = df_case_death['prob_cases'].astype('float')
    df_case_death['new_case'] = df_case_death['new_case'].astype('float')
    df_case_death['pnew_case'] = df_case_death['pnew_case'].astype('float')
    df_case_death['tot_death'] = df_case_death['tot_death'].astype('float')
    df_case_death['conf_death'] = df_case_death['conf_death'].astype('float')
    df_case_death['prob_death'] = df_case_death['prob_death'].astype('float')
    df_case_death['new_death'] = df_case_death['new_death'].astype('float')
    df_case_death['pnew_death'] = df_case_death['pnew_death'].astype('float')
    df_case_death['created_at'] = df_case_death['created_at'].astype('datetime64')
    
    #aggregating data based on submission date
    df_case_death_agg = df_case_death.groupby('submission_date', as_index=False).sum()

    df_case_death_agg['7d_ra_case'] = df_agg['new_case'].rolling(7).mean()
    df_case_death_agg['30d_ra_case'] = df_agg['new_case'].rolling(30).mean()
    df_case_death_agg['7d_ra_death'] = df_agg['new_death'].rolling(7).mean()
    df_case_death_agg['30d_ra_death'] = df_case_death_agg['new_death'].rolling(30).mean()

    # sorting data
    df_agg = df_agg.sort_values(by=['submission_date'], ascending=False, ignore_index=True)
    
    return df

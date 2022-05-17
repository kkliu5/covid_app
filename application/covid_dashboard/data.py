"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.tseries.offsets import MonthEnd
import requests
from sodapy import Socrata
from urllib.request import urlopen
import json
pd.options.mode.chained_assignment = None

"""Data Pulls"""
def create_case_death_df():
    """Case & Death Data ~20s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get_all("9mfq-cb36")
    df_case_death = pd.DataFrame.from_records(results)
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
    df_case_death_agg['7d_ra_case'] = df_case_death_agg['new_case'].rolling(7).mean()
    df_case_death_agg['30d_ra_case'] = df_case_death_agg['new_case'].rolling(30).mean()
    df_case_death_agg['7d_ra_death'] = df_case_death_agg['new_death'].rolling(7).mean()
    df_case_death_agg['30d_ra_death'] = df_case_death_agg['new_death'].rolling(30).mean()
    # sorting data
    df_case_death_agg = df_case_death_agg.sort_values(by=['submission_date'], ascending=False, ignore_index=True)
    
    return df_case_death_agg

"""HOSPITALZATION DATA"""
def create_hos_df():
    """Case Status ~2s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["current_status, count('cdc_case_earliest_dt')"], group = ["current_status"])
    df_hos_1 = pd.DataFrame.from_records(results)
    df_hos_1['current_status'] = df_hos_1['current_status'].astype('string')
    df_hos_1['count_cdc_case_earliest_dt'] = df_hos_1['count_cdc_case_earliest_dt'].astype('float')
    
    """Cases by Sex ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["sex, count('cdc_case_earliest_dt')"], group = ["sex"])
    df_hos_2 = pd.DataFrame.from_records(results)
    df_hos_2['sex'] = df_hos_2['sex'].astype('string')
    df_hos_2['count_cdc_case_earliest_dt'] = df_hos_2['count_cdc_case_earliest_dt'].astype('float')
    df_hos_2['sex'] = df_hos_2['sex'].str.replace('Unknown','Missing')
    df_hos_2['sex'] = df_hos_2['sex'].str.replace('NA','Missing')
    df_hos_2 = df_hos_2.groupby('sex', as_index=False).sum()
    
    """Cases by Age Group ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["age_group, count('cdc_case_earliest_dt')"], group = ["age_group"])
    df_hos_3 = pd.DataFrame.from_records(results)
    df_hos_3['age_group'] = df_hos_3['age_group'].astype('string')
    df_hos_3['count_cdc_case_earliest_dt'] = df_hos_3['count_cdc_case_earliest_dt'].astype('float')
    df_hos_3['age_group'] = df_hos_3['age_group'].str.replace('NA','Missing')
    df_hos_3 = df_hos_3.groupby('age_group', as_index=False).sum()
    
    """Cases by Race ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["race_ethnicity_combined, count('cdc_case_earliest_dt')"], group = ["race_ethnicity_combined"])
    df_hos_4 = pd.DataFrame.from_records(results)
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].astype('string')
    df_hos_4['count_cdc_case_earliest_dt'] = df_hos_4['count_cdc_case_earliest_dt'].astype('float')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('American Indian/Alaska Native, Non-Hispanic','American Indian/Alaska Native')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('Asian, Non-Hispanic','Asian')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('Black, Non-Hispanic','Black')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('Multiple/Other, Non-Hispanic','Multiple/Other')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('Native Hawaiian/Other Pacific Islander, Non-Hispanic','Native Hawaiian/Other Pacific Islander')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('White, Non-Hispanic','White')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('NA','Missing')
    df_hos_4['race_ethnicity_combined'] = df_hos_4['race_ethnicity_combined'].str.replace('Unknown','Missing')
    df_hos_4 = df_hos_4.groupby('race_ethnicity_combined', as_index=False).sum()
    
    """Case by Hospitalzation ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["hosp_yn, count('cdc_case_earliest_dt')"], group = ["hosp_yn"])
    df_hos_5 = pd.DataFrame.from_records(results)
    df_hos_5['hosp_yn'] = df_hos_5['hosp_yn'].astype('string')
    df_hos_5['count_cdc_case_earliest_dt'] = df_hos_5['count_cdc_case_earliest_dt'].astype('float')
    df_hos_5['hosp_yn'] = df_hos_5['hosp_yn'].str.replace('Unknown','Missing')
    df_hos_5 = df_hos_5.groupby('hosp_yn', as_index=False).sum()
    
    """ Cases by ICU ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["icu_yn, count('cdc_case_earliest_dt')"], group = ["icu_yn"])
    df_hos_6 = pd.DataFrame.from_records(results)
    df_hos_6['icu_yn'] = df_hos_6['icu_yn'].astype('string')
    df_hos_6['count_cdc_case_earliest_dt'] = df_hos_6['count_cdc_case_earliest_dt'].astype('float')
    df_hos_6['icu_yn'] = df_hos_6['icu_yn'].str.replace('Unknown','Missing')
    df_hos_6['icu_yn'] = df_hos_6['icu_yn'].str.replace('nul','Missing')
    df_hos_6 = df_hos_6.groupby('icu_yn', as_index=False).sum()
    
    """Cases by Death Status ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["death_yn, count('cdc_case_earliest_dt')"], group = ["death_yn"])
    df_hos_7 = pd.DataFrame.from_records(results)
    df_hos_7['death_yn'] = df_hos_7['death_yn'].astype('string')
    df_hos_7['count_cdc_case_earliest_dt'] = df_hos_7['count_cdc_case_earliest_dt'].astype('float')
    df_hos_7['death_yn'] = df_hos_7['death_yn'].str.replace('Unknown','Missing')
    df_hos_7 = df_hos_7.groupby('death_yn', as_index=False).sum()
    
    """Cases with Medical Status ~1s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("vbim-akqf", select = ["medcond_yn, count('cdc_case_earliest_dt')"], group = ["medcond_yn"])
    df_hos_8 = pd.DataFrame.from_records(results)
    df_hos_8['medcond_yn'] = df_hos_8['medcond_yn'].astype('string')
    df_hos_8['count_cdc_case_earliest_dt'] = df_hos_8['count_cdc_case_earliest_dt'].astype('float')
    df_hos_8['medcond_yn'] = df_hos_8['medcond_yn'].str.replace('Unknown','Missing')
    df_hos_8 = df_hos_8.groupby('medcond_yn', as_index=False).sum()
    
    """ICU Cases Over Time ~5s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get_all("vbim-akqf", select = ["icu_yn, cdc_case_earliest_dt, count('cdc_case_earliest_dt')"], group = ["icu_yn, cdc_case_earliest_dt"])
    df_hos_9 = pd.DataFrame.from_records(results)
    df_hos_9['icu_yn'] = df_hos_9['icu_yn'].astype('string')
    df_hos_9['cdc_case_earliest_dt'] = df_hos_9['cdc_case_earliest_dt'].astype('datetime64')
    df_hos_9['count_cdc_case_earliest_dt'] = df_hos_9['count_cdc_case_earliest_dt'].astype('float')
    df_hos_9 = df_hos_9[df_hos_9['icu_yn'] == 'Yes']

    """Hospitalized Cases Over Time ~2s"""
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get_all("vbim-akqf", select = ["hosp_yn, cdc_case_earliest_dt, count('cdc_case_earliest_dt')"], group = ["hosp_yn, cdc_case_earliest_dt"])
    df_hos_10 = pd.DataFrame.from_records(results)
    df_hos_10['hosp_yn'] = df_hos_10['hosp_yn'].astype('string')
    df_hos_10['cdc_case_earliest_dt'] = df_hos_10['cdc_case_earliest_dt'].astype('datetime64')
    df_hos_10['count_cdc_case_earliest_dt'] = df_hos_10['count_cdc_case_earliest_dt'].astype('float')
    df_hos_10 = df_hos_10[df_hos_10['hosp_yn'] == 'Yes']
    
    return df_hos_1, df_hos_2, df_hos_3, df_hos_4, df_hos_5, df_hos_6, df_hos_7, df_hos_8, df_hos_9, df_hos_10

"""TESTING DATA ~20s"""
def create_test_df():
    client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
    results = client.get("nra9-vzzn", limit = 100000000)
    df_test_1 = pd.DataFrame.from_records(results)
    
    pop_2019 = requests.get('https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=county').json()
    
    df_test_1['cases_per_100k_7_day_count'] = df_test_1['cases_per_100k_7_day_count'].str.replace('suppressed','0')
    df_test_1['cases_per_100k_7_day_count'] = df_test_1['cases_per_100k_7_day_count'].str.replace(',','')
    df_test_1['state_name'] = df_test_1['state_name'].astype('string')
    df_test_1['county_name'] = df_test_1['county_name'].astype('string')
    df_test_1['fips_code'] = df_test_1['fips_code'].astype('string')
    df_test_1['date'] = df_test_1['date'].astype('datetime64')
    df_test_1['cases_per_100k_7_day_count'] = df_test_1['cases_per_100k_7_day_count'].astype('float')
    df_test_1['percent_test_results_reported'] = df_test_1['percent_test_results_reported'].astype('float')
    df_test_1['community_transmission_level'] = df_test_1['community_transmission_level'].astype('string')
    df_test_1['cases_per_100k_7_day_count'] = df_test_1['cases_per_100k_7_day_count'].fillna(0)
    df_test_1['percent_test_results_reported'] = df_test_1['percent_test_results_reported'].fillna(0)
    col_names = pop_2019[0]
    pop_2019.pop(0)
    df_pop_19 = pd.DataFrame(pop_2019, columns=col_names)
    df_pop_19['fips_code'] = df_pop_19['state'] + df_pop_19['county']
    df_test_2 = df_test_1.merge(df_pop_19, left_on='fips_code', right_on='fips_code')
    df_test_2['population'] = df_test_2['POP']
    df_test_2 = df_test_2.drop(columns=['NAME', 'state', 'county', 'POP'])

    df_test_3 = df_test_2[df_test_2['percent_test_results_reported'].between(0.00001, .9999999)]
    df_test_3['percent_test_results_reported'] = df_test_3['percent_test_results_reported']*100
    df_test_4 = df_test_2[df_test_2['percent_test_results_reported'] == 0]
    df_test_5 = df_test_2[df_test_2['percent_test_results_reported'] >= 1]
    df_test_6 = df_test_3.append(df_test_4).append(df_test_5)

    df_test_6['population'] = df_test_6['population'].astype('float')
    df_test_6['pos_test_7_day'] = df_test_6['cases_per_100k_7_day_count'] / 100000 * df_test_6['population']
    df_test_6['tot_test_7_day'] = df_test_6['pos_test_7_day'] / (df_test_6['percent_test_results_reported']/100)
    df_test_6['tot_test_daily'] = df_test_6['tot_test_7_day'] / 7
    df_test_6.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_test_6['pos_test_7_day'] = df_test_6['pos_test_7_day'].fillna(0)
    df_test_6['tot_test_7_day'] = df_test_6['tot_test_7_day'].fillna(0)
    df_test_6['tot_test_daily'] = df_test_6['tot_test_daily'].fillna(0)

    df_test_agg = df_test_6.groupby('date', as_index=False).sum()

    df_test_agg['7d_ra_tot_test_daily'] = df_test_agg['tot_test_daily'].rolling(7).mean()
    df_test_agg['30d_ra_tot_test_daily'] = df_test_agg['tot_test_daily'].rolling(30).mean()
    
    return df_test_agg

""" VACCINE DATA"""    
# def create_vacc_df():
#     columns = ['date, fips, recip_county, recip_state, series_complete_pop_pct, series_complete_yes, booster_doses, booster_doses_vax_pct']
#     client = Socrata("data.cdc.gov", app_token="SMDNVaBjBRb2aY7ZjRLbnLpZc", username="kkliu5@gmail.com", password="R@gTug4WxVs#p5p")
#     results = client.get("8xkx-amqh", limit = 100000000)
#     df_vacc_1 = pd.DataFrame.from_records(results)
#     df_vacc_1['date'] = df_vacc_1['date'].astype('datetime64')
#     df_vacc_1['recip_county'] = df_vacc_1['recip_county'].astype('string')
#     df_vacc_1['recip_state'] = df_vacc_1['recip_state'].astype('string')
#     df_vacc_1['series_complete_pop_pct'] = df_vacc_1['series_complete_pop_pct'].astype('float')
#     df_vacc_1['series_complete_yes'] = df_vacc_1['series_complete_yes'].astype('float')
#     df_vacc_1['booster_doses'] = df_vacc_1['booster_doses'].astype('float')
#     df_vacc_1['booster_doses_vax_pct'] = df_vacc_1['booster_doses_vax_pct'].astype('float')

#     date_min = df_vacc_1['date'].min()
#     date_max = df_vacc_1['date'].max()
#     date_list = []
#     for mon in pd.date_range(date_min, date_max, freq='MS'):
#         date_list.append(mon.strftime("%Y-%m-%d"))
#     df_vacc_animated = df_vacc_1[df_vacc_1['date'].isin(date_list)]
#     df_vacc_static = df_vacc_1[df_vacc_1['date'] == date_max]
#     df_vacc_animated = df_vacc_animated.sort_values('date',ascending=True)
#     df_vacc_animated['date'] = df_vacc_animated['date'].astype('string')

#     with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#         counties = json.load(response)
    
#     return counties, df_vacc_static

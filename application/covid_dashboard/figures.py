import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

from .data import create_case_death_df
from .data import create_test_df
from .data import create_vacc_df
from .data import create_hos_df

# Load DataFrame
df_case_death_agg = create_case_death_df()
df_test_agg = create_test_df()
counties, df_vacc_animated, df_vacc_static = create_vacc_df()
df_hos_1, df_hos_2, df_hos_3, df_hos_4, df_hos_5, df_hos_6, df_hos_7, df_hos_8, df_hos_9, df_hos_10 = create_hos_df()

# Graphing Functions
def customlegend(fig, new_legend):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                fig.data[i].name = new_legend[fig.data[i].name]
    return(fig)

def fig_format(fig):
    #fig.update_xaxes(rangeslider=dict(visible=True))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(font_color= 'white', xaxis_title='Date', yaxis_title='Amount', legend_title_text='Variable')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(title={'y':0.85,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    return(fig)

#Figures/Graphs
"""Daily Cases"""
case_fig = px.line(df_case_death_agg, x='submission_date', y=['new_case','7d_ra_case','30d_ra_case'],
                   labels={"value":"Cases", "submission_date":"Date"},
                   title=('Daily Cases'))
case_fig = customlegend(fig = case_fig,
                        new_legend = {'new_case':'Daily Case',
                                      '7d_ra_case': '7 Day Rolling Average',
                                      '30d_ra_case': '30 Day Rolling Average'})
fig_format(case_fig)
case_fig.show()

"""Daily Deaths"""
death_fig = px.line(df_case_death_agg, x='submission_date', y=['new_death','7d_ra_death','30d_ra_death'],
                   labels={"value":"Deaths", "submission_date":"Date"},
                   title=('Daily Deaths'))
death_fig = customlegend(fig = death_fig,
                        new_legend = {'new_death':'Daily Death',
                                      '7d_ra_death': '7 Day Rolling Average',
                                      '30d_ra_death': '30 Day Rolling Average'})
fig_format(death_fig)
death_fig.show()

"""Daily Tests"""
test_fig = px.bar(df_test_agg, x='date', y=['tot_test_daily'],
                 labels={"value":"Tests", "date":"Date"},
                 title=('Daily Tests'))
test_fig = customlegend(fig = test_fig,
                        new_legend = {'tot_test_daily':'Daily Test'})
fig_format(test_fig)
test_fig.show()

"""Animated Vaccine Map"""
#creating map that displays percent vaccinated by county over time
animated_map = px.choropleth_mapbox(df_vacc_animated, geojson=counties, locations='fips', color='series_complete_pop_pct',
                           animation_frame='date',
                           color_continuous_scale="Viridis",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'series_complete_pop_pct':'Vaccinated Percentage',
                                  'date':'Date',
                                  'fips':'FIPS Code'}
                          )
animated_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
animated_map.show()

#Static Vaccine Map
#creating map that displays percent vaccinated by county currently
current_map = px.choropleth_mapbox(df_vacc_static, geojson=counties, locations='fips', color='series_complete_pop_pct',
                           color_continuous_scale="Viridis",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'series_complete_pop_pct':'Vaccinated Percentage',
                                  'date':'Date',
                                  'fips':'FIPS Code'}
                          )
animated_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
animated_map.show()

"""Case Status"""
hos_case_fig = px.bar(df_hos_1, 
             x='current_status', 
             y='count_cdc_case_earliest_dt',
             labels={"current_status": "Current Status",  "count_cdc_case_earliest_dt": "Count of Cases"},
             title=('Cases'))
"""Cases by Sex"""
hos_sex_fig = px.bar(df_hos_2, x='sex', y='count_cdc_case_earliest_dt',
            labels={"sex": "Sex",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Sex'))
"""Cases by Age Group"""
hos_age_fig = px.bar(df_hos_3, x='age_group', y='count_cdc_case_earliest_dt',
            labels={"age_group": "Age Group",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Age Group')
            )
"""Cases by Race"""
hos_race_fig = px.bar(df_hos_4, x='race_ethnicity_combined', y='count_cdc_case_earliest_dt',
            labels={"race_ethnicity_combined": "Race",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Race')
            )
"""Case by Hospitalzation"""
hos_hos_fig = px.bar(df_hos_5, x='hosp_yn', y='count_cdc_case_earliest_dt',
            labels={"hosp_yn": "Hospitalized",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Hospitalzation Status')
            )
""" Cases by ICU"""
hos_icu_fig = px.bar(df_hos_6, x='icu_yn', y='count_cdc_case_earliest_dt',
            labels={"icu_yn": "ICU Status",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by ICU Status')
            )
"""Cases by Death Status"""
hos_death_fig = px.bar(df_hos_7, x='death_yn', y='count_cdc_case_earliest_dt',
            labels={"death_yn": "Death Status",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Death Status')
            )
"""Cases with Medical Status"""
hos_med_fig = px.bar(df_hos_8, x='medcond_yn', y='count_cdc_case_earliest_dt',
            labels={"medcond_yn": "Medical Status",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Cases by Presence of Underlying Comorbidity or Disease')
            )
"""ICU Cases Over Time"""
hos_icu_ts_fig = px.line(df_hos_9, x='cdc_case_earliest_dt', y='count_cdc_case_earliest_dt',
            labels={"cdc_case_earliest_dt": "Date",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('ICU Cases over Time')
"""Hospitalized Cases Over Time"""
hos_hos_ts_fig = px.line(df_hos_10, x='cdc_case_earliest_dt', y='count_cdc_case_earliest_dt',
            labels={"cdc_case_earliest_dt": "Date",  "count_cdc_case_earliest_dt": "Count of Cases"},
            title=('Hospitalized Cases over Time')
            )
              

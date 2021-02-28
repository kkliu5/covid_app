import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

from .data import create_dataframe

# Load DataFrame
df = create_dataframe()

# Graphing Functions
def customlegend(fig, new_legend):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                fig.data[i].name = new_legend[fig.data[i].name]
    return(fig)

def fig_format(fig):
    fig.update_xaxes(rangeslider=dict(visible=True))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(font_color= 'white', xaxis_title='Date', yaxis_title='Amount', legend_title_text='Variable')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return(fig)

#Figures/Graphs
#positive increase
fig_pos_test_in = px.line(df, x='date', y=['positiveIncrease', '7d_ra_pos_in', '30d_ra_pos_in'],
                          title='Daily Change in Positive Covid-19 Cases',
                          template = 'simple_white')
fig_format(fig_pos_test_in)
fig_pos_test_in = customlegend(fig = fig_pos_test_in,
                               new_legend = {'positiveIncrease':'Positive Increase',
                                             '7d_ra_pos_in': '7 Day Rolling Average',
                                             '30d_ra_pos_in': '30 Day Rolling Average'
                                             })

# hospital increase
fig_hos_in = px.line(df, x='date', y=['hospitalizedIncrease', '7d_ra_hos_in', '30d_ra_hos_in'],
                     title='Daily Change in Covid-19 Hospitalzations',
                     template = 'simple_white')
fig_format(fig_hos_in)
fig_hos_in = customlegend(fig = fig_hos_in,
                               new_legend = {'hospitalizedIncrease':'Hospitalization Increase',
                                             '7d_ra_hos_in': '7 Day Rolling Average',
                                             '30d_ra_hos_in': '30 Day Rolling Average'
                                             })

# death increase
fig_dth_in = px.line(df, x='date', y=['deathIncrease', '7d_ra_dth_in', '30d_ra_dth_in'],
                     title='Daily Change in Deaths Due to Covid-19',
                     template = 'simple_white')
fig_format(fig_dth_in)
fig_dth_in = customlegend(fig = fig_dth_in,
                               new_legend = {'deathIncrease':'Death Increase',
                                             '7d_ra_dth_in': '7 Day Rolling Average',
                                             '30d_ra_dth_in': '30 Day Rolling Average'
                                             })

# negative increase - not used
fig_neg_test_in = px.line(df, x='date', y=['negativeIncrease', '7d_ra_neg_in', '30d_ra_neg_in'],
                            title='Negative Increase',
                          template='none')
fig_neg_test_in.update_xaxes(rangeslider=dict(visible=True))

# total results increase - not used
fig_tot_test_in = px.line(df, x='date', y=['totalTestResults', '7d_ra_tot_res_in', '30d_ra_tot_res_in'],
                            title='Total Test Results Increase')
fig_tot_test_in.update_xaxes(rangeslider=dict(visible=True))



# Cumulative testing results 
fig_cum_test = px.line(df, x='date', y=['positive','negative','totalTestResults'],
                     title='Cumulative Testing Results',
                     template = 'simple_white')
fig_format(fig_cum_test)
fig_cum_test = customlegend(fig = fig_cum_test,
                               new_legend = {'positive':'Positive Results',
                                             'negative': 'Negative Results',
                                             'totalTestResults': 'Total Testing Results'
                                             })

# Cumulative hospitalized results 
fig_cum_hos = px.line(df, x='date', y=['hospitalizedCumulative','inIcuCumulative','onVentilatorCumulative'],
                     title='Cumulative Hospitalized Due to Covid-19',
                     template = 'simple_white')
fig_format(fig_cum_hos)
fig_cum_hos = customlegend(fig = fig_cum_hos,
                               new_legend = {'hospitalizedCumulative':'Total Hospitalized',
                                             'inIcuCumulative': 'Total in ICU',
                                             'onVentilatorCumulative': 'Total on Ventilator'
                                             })

# Cumulative death results 
fig_cum_dth = px.line(df, x='date', y=['death'],
                     title='Cumulative Deaths Due to Covid-19',
                     template = 'simple_white')
fig_format(fig_cum_dth)
fig_cum_dth = customlegend(fig = fig_cum_dth,
                               new_legend = {'death':'Deaths'})



#Rates
#Positive Rate (Positive cases/Total cases)
fig_pos_rate = px.line(df, x='date', y=['positive_rate'],
                       title='Positive Rate',
                       template = 'simple_white')
fig_format(fig_pos_rate)
fig_pos_rate = customlegend(fig = fig_pos_rate,
                               new_legend = {'positive_rate':'Positive Rate'
                                             })

#Negative Rate (Negative cases/Total cases)
fig_neg_rate = px.line(df, x='date', y=['negative_rate'],
                       title='Negative Rate',
                       template = 'simple_white')
fig_format(fig_neg_rate)
fig_neg_rate = customlegend(fig = fig_neg_rate,
                               new_legend = {'negative_rate':'Negative Rate'
                                             })

#Pending Rate (Pending cases/Total cases) - Not Used
fig_pen_rate = px.line(df, x='date', y=['pending_rate'],
                       title='Pending Rate',
                       template = 'simple_white')
fig_format(fig_pen_rate)
fig_pen_rate = customlegend(fig = fig_pen_rate,
                               new_legend = {'pending_rate':'Pending Rate'
                                             })

#Hospitalized Rate (Hospitalized cases/Positive cases)
fig_hos_rate = px.line(df, x='date', y=['hospitalized_rate'],
                       title='Hospitalized Rate',
                       template = 'simple_white')
fig_format(fig_hos_rate)
fig_hos_rate = customlegend(fig = fig_hos_rate,
                               new_legend = {'hospitalized_rate':'Hospitalized Rate'
                                             })

#ICU Rate (ICU cases/Positive cases) - Not Used
fig_icu_rate = px.line(df, x='date', y=['ICU_rate'],
                       title='ICU Rate',
                       template = 'simple_white')
fig_format(fig_icu_rate)
fig_icu_rate = customlegend(fig = fig_icu_rate,
                               new_legend = {'ICU_rate':'ICU Rate'
                                             })

#Ventilator Rate (Positive cases/Positive cases) - Not Used
fig_ven_rate = px.line(df, x='date', y=['ventilator_rate'],
                       title='Ventalator Rate',
                       template = 'simple_white')
fig_format(fig_ven_rate)
fig_ven_rate = customlegend(fig = fig_ven_rate,
                               new_legend = {'ventilator_rate':'Ventilator Rate'
                                             })

#Death Rate (Deaths/Positive cases)
fig_dth_rate = px.line(df, x='date', y=['death_rate'],
                       title='Death Rate',
                       template = 'simple_white')
fig_format(fig_dth_rate)
fig_dth_rate = customlegend(fig = fig_dth_rate,
                               new_legend = {'death_rate':'Death Rate'
                                             })

#ICU Rate based on Hospitalzations (ICU cases/Hospitalized cases)
fig_hos_icu_rate = px.line(df, x='date', y=['hos_ICU_rate'],
                           title='ICU Rate Realative to Hospitalzations Due to Covid-19',
                           template = 'simple_white')
fig_format(fig_hos_icu_rate)
fig_hos_icu_rate = customlegend(fig = fig_hos_icu_rate,
                               new_legend = {'hos_ICU_rate':'ICU Rate'
                                             })

#Ventilator Rate based on Hospitalzations (Positive cases/Hospitalized cases) 
fig_hos_ven_rate = px.line(df, x='date', y=['hos_ventilator_rate'],
                           title='Ventalator Rate Realative to Hospitalzations Due to Covid-19',
                           template = 'simple_white')
fig_format(fig_hos_ven_rate)
fig_hos_ven_rate = customlegend(fig = fig_hos_ven_rate,
                               new_legend = {'hos_ventilator_rate':'Ventilator Rate'
                                             })

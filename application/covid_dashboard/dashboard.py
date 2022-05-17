"""Instantiate a Dash app."""
import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
from datetime import datetime

from .data import *
from .figures import *

# Load DataFrame
df_case_death_agg = create_case_death_df()
df_test_agg = create_test_df()
# Variables
new_cases = df_case_death_agg['new_case'][0]
total_cases = df_case_death_agg['tot_cases'][0]
new_tests_df = df_test_agg.loc[df_test_agg['tot_test_daily'] > 0].sort_values(by=['date'], ascending=False, ignore_index=True)
new_tests = new_tests_df['tot_test_daily'][0]
total_tests = df_test_agg['tot_test_daily'].sum()
new_deaths = df_case_death_agg['new_death'][0]
total_deaths = df_case_death_agg['tot_death'][0]
last_update = datetime.date(df_case_death_agg['submission_date'][0])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/",
        external_stylesheets=[dbc.themes.SUPERHERO],
    )
    
    dash_app.title = 'Covid-19 Dashboard'
    
    #lo Create Layout
    dash_app.layout = dbc.Container(
        [
            html.H1("USA Covid-19 Dashboard"),
            html.P(children=['Last updated: ',last_update], style={'text-align': 'right'}),
            html.Hr(),
            dbc.Tabs(
                [
                    dbc.Tab(label="Overview", tab_id="tab-1"),
#                     dbc.Tab(label="Vaccination", tab_id="tab-2"),
                    dbc.Tab(label="Testing", tab_id="tab-3"),
                    dbc.Tab(label="Hospitalizations", tab_id="tab-4"),
                    dbc.Tab(label="Deaths", tab_id="tab-5"),
                    dbc.Tab(label="About", tab_id="tab-6"),
                    ],
                id = 'tabs',
                active_tab = 'tab-1',
                ),
            html.Div(id="tab-content", className="p-4"),
            html.Br(),
            html.Div(id="drop_figure"),
            ]
        )
    init_callbacks(dash_app)
    
    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(Output("tab-content", "children"),[Input("tabs", "active_tab")])
    
    def render_tab_content(active_tab):
        if active_tab is not None:
            if active_tab == "tab-1":
                return (dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content('Cases', new_cases, total_cases),
                                         #style = {"width": "16rem"},
                                         color = "primary"
                                         )),
                        dbc.Col(dbc.Card(card_content('Tests', new_tests, total_tests),
                                         #style = {"width": "16rem"},
                                         color = "secondary"
                                         )),
                        dbc.Col(dbc.Card(card_content('Deaths', new_deaths, total_deaths),
                                         #style = {"width": "16rem"},
                                         color = "danger"
                                         )),
                    ]
                ),
                        html.Br(),
                        html.Div([
                            dcc.Dropdown(
                                id='demo-dropdown',
                                options=[
                                    {'label': 'New Cases', 'value': 'C'},
                                    {'label': 'New Hospitalzations', 'value': 'H'},
                                    {'label': 'New Deaths', 'value': 'D'}
                                ],
                                style=
                                    {
                                        #'width': '150px',
                                        'color': '#000000',
                                        'background-color': '#DCDCDC',
                                     },
                                value='C',
                                clearable=False,
                                searchable=False
                            ),
                        html.Div(id='dd-output-container')]),
                        html.Br(),
#                         dcc.Graph(id='current_map', figure=current_map)
                        )
#             elif active_tab == "tab-2":
#                 return (
#                     dcc.Graph(id='animated_map', figure=animated_map)
#                     )
            elif active_tab == "tab-3":
                return (
                    dcc.Graph(id='test_fig', figure=test_fig)
                    )
            elif active_tab == "tab-4":
                return (
                    dcc.Graph(id='hos_case_fig', figure=hos_case_fig),
                    html.Br(),
                    dcc.Graph(id='hos_sex_fig', figure=hos_sex_fig),
                    html.Br(),
                    dcc.Graph(id='hos_age_fig', figure=hos_age_fig),
                    html.Br(),
                    dcc.Graph(id='hos_race_fig', figure=hos_race_fig),
                    html.Br(),
                    dcc.Graph(id='hos_hos_fig', figure=hos_hos_fig),
                    html.Br(),
                    dcc.Graph(id='hos_icu_fig', figure=hos_icu_fig),
                    html.Br(),
                    dcc.Graph(id='hos_death_fig', figure=hos_death_fig),
                    html.Br(),
                    dcc.Graph(id='hos_med_fig', figure=hos_med_fig),
                    html.Br(),
                    dcc.Graph(id='hos_icu_ts_fig', figure=hos_icu_ts_fig),
                    html.Br(),
                    dcc.Graph(id='hos_hos_ts_fig', figure=hos_hos_ts_fig),
                    html.Br()
                    )
            elif active_tab == "tab-5":
                return (
                    dcc.Graph(id='death_fig', figure=death_fig),
                    )
            elif active_tab == "tab-6":
                return (
                    html.H4("Dashboard Information"),
                    html.Br(),
                    html.Div([
                        html.P(["This dashboard is coded in Python by Kevin Liu through the use of ",
                                html.A("Plotly",
                                       href='https://plotly.com', target="_blank"),
                                " and ",
                                html.A("Dash.",
                                       href='https://plotly.com/dash/', target="_blank"),
                                ]),
                        ]),
                    html.Div([
                        html.P(["The data scource comes from the ",
                                html.A("CDC.",
                                       href='https://data.cdc.gov', target="_blank"),
                                ]),
                        ]),
                    html.Div([
                        html.P(["The dashboard is hosted on a Raspberry Pi through the use of ",
                                html.A("NGINX",
                                       href='https://nginx.com', target="_blank"),
                                " and ",
                                html.A("Gunicorn.",
                                       href='https://gunicorn.org', target="_blank"),
                                ]),
                        ]),
                    )
                        
        return "No tab selected"
    
    @dash_app.callback(
        dash.dependencies.Output('dd-output-container', 'children'),
        [dash.dependencies.Input('demo-dropdown', 'value')])
        
    def update_output(value):
        if value == 'C':
            return dcc.Graph(id='case_fig', figure=case_fig)
        elif value == 'H':
            return dcc.Graph(id='hos_hos_ts_fig', figure=hos_hos_ts_fig)
        elif value == 'D':
            return dcc.Graph(id='death_fig', figure=death_fig)
    
# # Dash Items
def card_content(card_name, card_new_value, card_total_value):
    card = [
        dbc.CardHeader(
            [
                html.H2(card_name, style={'text-align': 'center'}, className="card-sub-header"),
                ]
            ),
        dbc.CardBody(
            [
                html.H4(children=['New : ', f"{int(card_new_value):,}"],
                        #style={'text-align': 'right'},
                        className="card-sub-body"
                        ),
                html.H4(children=['Total : ', f"{int(card_total_value):,}"],
                        #style={'text-align': 'right'},
                        className="card-sub-body2"
                       ),
                ]
            ),
#        dbc.CardFooter(
#            [
#                html.P(f"{int(card_total_value):,}", className="card-sub-footer"),
#            ]
#        ),
    ]
    return card


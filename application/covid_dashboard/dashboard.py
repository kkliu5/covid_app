"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
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
df_case_death_agg = df_case_death_agg.sort_values(by=['submission_date'], ascending=False, ignore_index=True)
new_cases = df_case_death_agg['new_case'][0]
total_cases = df_case_death_agg['tot_cases'][0]
new_deaths = df_case_death_agg['new_death'][0]
total_deaths = df_case_death_agg['tot_death'][0]
last_update = datetime.date(df_case_death_agg['submission_date'][0])
df_test_agg_1 = df_test_agg.loc[df_test_final['tot_test_daily'] > 0].sort_values(by=['date'], ascending=False, ignore_index=True)
new_tests = df_test_agg['tot_test_daily'].sum()

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
                    dbc.Tab(label="Vaccinations", tab_id="tab-2"),
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
                                    {'label': 'Positive Tests', 'value': 'PT'},
                                    {'label': 'Hospitalized', 'value': 'H'},
                                    {'label': 'Deaths', 'value': 'D'}
                                ],
                                style=
                                    {
                                        #'width': '150px',
                                        'color': '#000000',
                                        'background-color': '#DCDCDC',
                                     },
                                value='PT',
                                clearable=False,
                                searchable=False
                            ),
                        html.Div(id='dd-output-container')
                    ])
                        )
            elif active_tab == "tab-2":
                return html.Br(),
                    dcc.Graph(id='animated_map', figure=animated_map),
            elif active_tab == "tab-3":
                return (html.Br(),
                    dcc.Graph(id='test_fig', figure=test_fig),
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "Positive Rate Calculation",
#                                     id="collapse-button-1",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative positive results / Cumulative test results = Positive rate")),
#                                     id="collapse-1",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_neg_rate', figure=fig_neg_rate),
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "Negative Rate Calculation",
#                                     id="collapse-button-2",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative negative results / Cumulative test results = Negative rate")),
#                                     id="collapse-2",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_cum_test', figure=fig_cum_test)
#                     )
            elif active_tab == "tab-4":
                return (
                    dcc.Graph(id='hos_case_fig', figure=hos_case_fig),
                    dcc.Graph(id='hos_sex_fig', figure=hos_sex_fig),
                    dcc.Graph(id='hos_age_fig', figure=hos_age_fig),
                    dcc.Graph(id='hos_race_fig', figure=hos_race_fig),
                    dcc.Graph(id='hos_hos_fig', figure=hos_hos_fig),
                    dcc.Graph(id='hos_icu_fig', figure=hos_icu_fig),
                    dcc.Graph(id='hos_death_fig', figure=hos_death_fig),
                    dcc.Graph(id='hos_death_fig', figure=hos_med_fig),
                    dcc.Graph(id='hos_death_fig', figure=hos_icu_ts_fig),
                    dcc.Graph(id='hos_death_fig', figure=hos_hos_ts_fig)
                    
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "Hospitalized Rate Calculation",
#                                     id="collapse-button-3",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative hospitalized results / Cumulative positive test results = Hospitalized rate")),
#                                     id="collapse-3",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_hos_icu_rate', figure=fig_hos_icu_rate),
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "ICU Rate Calculation",
#                                     id="collapse-button-4",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative ICU patients / Cumulative hospitalized patients = ICU rate")),
#                                     id="collapse-4",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_hos_ven_rate', figure=fig_hos_ven_rate),
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "Ventilator Rate Calculation",
#                                     id="collapse-button-5",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative ventilator patients / Cumulative hospitalized patients = Ventilator rate")),
#                                     id="collapse-5",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_cum_hos', figure=fig_cum_hos)
                    )
            elif active_tab == "tab-5":
                return (
                    dcc.Graph(id='death_fig', figure=death_fig),
#                     html.Div(
#                             [
#                                 dbc.Button(
#                                     "Death Rate Calculation",
#                                     id="collapse-button-6",
#                                     className="mb-3",
#                                     color="primary",
#                                 ),
#                                 dbc.Collapse(
#                                     dbc.Card(dbc.CardBody("Cumulative dead / Cumulative positive results = Death rate")),
#                                     id="collapse-6",
#                                 ),
#                             ]
#                         ),
#                     dcc.Graph(id='fig_cum_death', figure=fig_cum_dth)
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
                        html.P(["The data scource comes from ",
                                html.A("CDC",
                                       href='https://covidtracking.com', target="_blank"),
#                                 html.Li(["Note that data collection through The COVID Tracking Project will end on March 7, 2021 as explained in this ",
#                                 html.A("post.",
#                                        href='https://covidtracking.com/analysis-updates/covid-tracking-project-end-march-7', target="_blank"),
#                                  ])
#                                 ]),
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
        if value == 'PT':
            return dcc.Graph(id='case_fig', figure=case_fig)
        elif value == 'H':
            return dcc.Graph(id='animated_map', figure=animated_map)
        elif value == 'D':
            return dcc.Graph(id='death_fig', figure=death_fig)
    
#     @dash_app.callback(Output("collapse-1","is_open"),[Input("collapse-button-1","n_clicks")],[State("collapse-1","is_open")],)
#     def toggle_collapse_1(n_1, is_open):
#         if n_1:
#             return not is_open
#         return is_open
    
#     @dash_app.callback(Output("collapse-2","is_open"),[Input("collapse-button-2","n_clicks")],[State("collapse-2","is_open")],)
    
#     def toggle_collapse_2(n_2, is_open):
#         if n_2:
#             return not is_open
#         return is_open
    
#     @dash_app.callback(Output("collapse-3","is_open"),[Input("collapse-button-3","n_clicks")],[State("collapse-3","is_open")],)
    
#     def toggle_collapse_2(n_3, is_open):
#         if n_3:
#             return not is_open
#         return is_open
    
#     @dash_app.callback(Output("collapse-4","is_open"),[Input("collapse-button-4","n_clicks")],[State("collapse-4","is_open")],)
    
#     def toggle_collapse_2(n_4, is_open):
#         if n_4:
#             return not is_open
#         return is_open
    
#     @dash_app.callback(Output("collapse-5","is_open"),[Input("collapse-button-5","n_clicks")],[State("collapse-5","is_open")],)
    
#     def toggle_collapse_2(n_5, is_open):
#         if n_5:
#             return not is_open
#         return is_open
    
#     @dash_app.callback(Output("collapse-6","is_open"),[Input("collapse-button-6","n_clicks")],[State("collapse-6","is_open")],)
    
#     def toggle_collapse_2(n_6, is_open):
#         if n_6:
#             return not is_open
#         return is_open

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


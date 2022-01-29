import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
from datetime import date,datetime, timedelta

cred = credentials.Certificate('C:\\Users\\nimal\\eHealth-EMS\\hit-with-database-794dbb2c512f.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#---------------above is nursetlayout_for_nurse--------------below is patientlayout--------------

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


patient_array = []
patient_id_array = []
curr_patient_id = ''

layoutpatient= dbc.Container([
    html.H1(children='Patients List'),
    dbc.Button("Back",id="back_P",color="link", style={'margin-left': '-10px','background-color':'#eef2f6','color':'black', 'border':''},className="me-1",n_clicks=0),
    html.Br(),
    dbc.Button('Add New Patient', id='button_P',
    style={'display': 'inline-block','border':'none','background-color':'#eef2f6','color':'black','margin-left': '982px','height': '33px'}),
    dt.DataTable(
        id='tblp',
        columns=[{"name": "Name", "id": "name"}, {"name": "Patient ID", "id": "patient_id"},
        {"name": "Risk Score", "id": "risk_score"}, {"name": "View Dashboard", "id": "dashboard_link"}],
        style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    style_as_list_view=True,
    filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
    ),
    dbc.Alert(id='tbl_outp'),
    dbc.Modal(
            [
                dbc.ModalBody(html.Embed(src='https://ktong2023.github.io/test/',height="500",width="470",style={'matgin-top':'400vw'})),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_P", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalp",
            is_open=False,
        ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Location( id='link_P',href='',refresh=False)
])

#---------------Patient_Dashboard_Below---------------#
#message shortcuts
shortcut1='Hi, you have an upcoming appointment'
shortcut2='Please complete the survey: https://padnim14.github.io/patient-survey/'
shortcut3='Your medicine is ready to pick up'

patientDashboard = html.Div([

    html.H1(id='patient_name',children=[], style={'text-align': 'left','margin-left': '2%'}),
    dcc.Link("Back to patients",href='/patients',refresh=True,style={'color':'black','text-align': 'left','margin-left': '2%'}),
    html.Br(),html.Hr(),
    dcc.Link("Schedule appointment",href='/appointment',style={'text-align': 'left','margin-left': '2%'}),
    dbc.Button('Send text message',id='send_sms',n_clicks=0,style={'text-align': 'left','margin-left': '2%','border':'none',"background":'#ffffff','color':'black'}),
    html.Hr(),
    html.Div([
                html.H4(id='patient_age',children=[], style={'text-align': 'left','margin-left': '2%'}),
    ],style={'display': 'inline-block', 'vertical-align': 'top','margin-left': '2%'}),
    html.Div(children=[
                        html.Embed(id='question',src="https://padnim14.github.io/patient-survey/" , 
                            width="700", height="400", style={'border':'1px silver solid'}) ], 
    style={'display': 'inline-block', 'margin-left': '51vw', 'margin-top': '-2%'}),
    html.Hr(style={'width':'90%','color':'black'}),
    html.Div(children=[
        dcc.Graph(id='plot_scatter',style={'display': 'inline-block'}),
        dcc.Graph(id='plot_bar',style={'display': 'inline-block'}) ],
        style={ 'vertical-align': 'top', 'margin-right': '0vw', 'margin-bottom': '3vh'}),
    dbc.Modal([
                dbc.ModalBody([
                    dbc.Container([
                                html.H3("Send text message", style={'padding':'5px'}),
                                html.Br(),
                                dcc.Dropdown(
                                    id='shortcuts',
                                    options=[
                                        {'label': shortcut1, 'value': shortcut1},
                                        {'label': shortcut2, 'value': shortcut2},
                                        {'label': shortcut3, 'value': shortcut3}
                                    ],
                                    placeholder='Select one short cut to send',
                                    style={'width':'100%','padding':'5px'}
                                ),
                                html.Br(),html.Br(),
                                dcc.Input(id='custom_txt',type="text", placeholder="Or send a custom message",debounce=True, 
                                persistence=False,style={'margin-left':'5px','width':'98%','padding':'10px'}),
                                html.Br(),html.Br(),html.Hr(),
                                dbc.Button("Send",id="send_message",n_clicks=0,style={'display': 'block','margin-left':'45%',}),
                                dcc.ConfirmDialog(
                                    id='confirmation_sms',
                                    message='Text message sent successfully',
                                )
                         ]),
                    ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_MC", className="ml-auto", n_clicks=0)
                ),
            ],
            id="MessageCenter",
            is_open=False,style={'width':'100%'}
        ),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0),
    dcc.Location( id='link_D',href='',refresh=False)
]) 

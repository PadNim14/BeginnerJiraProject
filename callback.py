import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import plotly.express as px  
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
from app import app
from layout import db, patient_array, patient_id_array, curr_patient_id
from twilio.rest import Client
# from apiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import date,datetime, timedelta

token =0

# # patient list # #

#feeding data to patient list
@app.callback(Output('tblp', 'data'), Input('interval-component', 'n_intervals'))
def refresh_patient_table(interval):
    global patient_id_array

    patient_id_array = []
    patient_array = []

    query = db.collection('patients').stream()

    for doc in query:
        patient_array.append(doc.to_dict())
        patient_id_array.append(doc.id)

    return patient_array

@app.callback(
    Output("modalp", "is_open"),
    [Input("button_P", "n_clicks"), Input("close_P", "n_clicks")],
    [State("modalp", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#link patientlist to patientDashboard and back button to nurselist
@app.callback(
    Output('link_P','href'),Output('link_P','refresh'),
    Input('back_P', 'n_clicks'),Input('tblp', 'active_cell') )
def patientlist_nav(n_clicks,active_cell):
    global token
    # if n_clicks!=0:
    #     if token == 1:
    #         return ('/nurses-admin', True)
    #     else:
    #         return ('/nurses', True)
    if search("dashboard_link", str(active_cell)):
        global curr_patient_id
        curr_patient_id = patient_id_array[active_cell["row"]]
        return ('/dashboard/' + curr_patient_id, True)

    else:
        return ('',False)

# # patient dashboard # #
@app.callback(
    Output('plot_scatter', 'figure'),
    Output('plot_bar','figure'),
    Input('interval-component', 'n_intervals'))
def plotgraphs(n):

    dfscat = pd.read_csv('ID 1003_heartrate_1min_20171001_20171007.csv')
    fig_scat = px.scatter(dfscat, x="Time", y="Value",title='Heart Rate')

    dfsbar = pd.read_csv('ID 1003_hourlyCalories_20171001_20171007.csv')
    fig_bar = px.bar(dfsbar, x="ActivityHour", y="Calories",title='Calories')

    return fig_scat,fig_bar

@app.callback(
    Output('patient_name', 'children'),
    Output('patient_age', 'children'),
    Input('interval-component', 'n_intervals'))
def patientinfo(n):
    global curr_patient_id

    #query = db.collection(u'nurses').document(u'B12v6a5o3dGXGId8g02j').collection('patients').document(u'00ovyLEhdfps05n58MtA')
    query = db.collection(u'patients').document(curr_patient_id)
    patientdata= query.get()
    #print(patientdata.to_dict())
    return (str(patientdata.to_dict().get('name')),
           "Age:" + str(patientdata.to_dict().get('age')) )

account_sid = 'AC18f4cc68aa19dffc73cf35a14b240990'
auth_token = '6bf7a8633d5c69f11314decadc9f3310'
client = Client(account_sid, auth_token)

#sending text message
@app.callback(
    Output('confirmation_sms', 'displayed'),Output('shortcuts', 'value'),Output('custom_txt', 'value'),
    Output('send_message', 'n_clicks'),
    Input('shortcuts', 'value'),Input('custom_txt','value'),Input('send_message','n_clicks'))
def send_text(shortcut, custom_txt,n_clicks):
    if (n_clicks>0) & (custom_txt is not None):
            message = client.messages \
                                .create(
                                    body=custom_txt,
                                    from_='+12078257270',
                                    to='+17172030525'
                                )
            return (True,None,None,0)
    if (n_clicks>0) & (shortcut is not None):
            message = client.messages \
                                .create(
                                    body=shortcut,
                                    from_='+12078257270',
                                    to='+17172030525'
                                )
            return (True,None,None,0)
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('MessageCenter', 'is_open'), Output('close_MC', 'n_clicks'), Output('send_sms', 'n_clicks'),
    Input('send_sms', 'n_clicks'),Input('close_MC', 'n_clicks'),
    [State('MessageCenter', 'is_open')])
def toggle_Message_Center(send_sms_n_clicks, close_MC_n_clicks, is_open):
    if send_sms_n_clicks>0 or close_MC_n_clicks>0:
        return (not is_open, 0,0)
    else:
        raise dash.exceptions.PreventUpdate


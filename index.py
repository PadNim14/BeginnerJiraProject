import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
from firebase_admin import credentials
from firebase_admin import firestore

from app import app
from layout import layoutpatient,patientDashboard
import callback


# padding for the page content
CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
    "background-color": "#eef2f6",
}


app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='page-content',children=[])
])

@app.callback(Output('page-content', 'children'),Output('page-content', 'style'),Output('url','href'),
              Input('url', 'pathname'))
def display_page(pathname): 
    if '/patients' in pathname:
         return (layoutpatient,CONTENT_STYLE,'')
    if  '/dashboard' in pathname:
         return (patientDashboard,{'':''},'')
    else:
        return (layoutpatient,CONTENT_STYLE,'')           

if __name__ == '__main__':
    app.run_server(debug=False)

    
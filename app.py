import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import requests
import os
from flask import Flask, send_from_directory

from func.func import func

import plotly.graph_objects as go
# colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,"assets")

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)

statelist=[]
todos['statewise'][0]['state']='INDIA'
for i in range(0,len(todos['statewise'])):
	statelist.append(todos['statewise'][i]['state'])
app = dash.Dash(assets_folder=STATIC_DIR, external_stylesheets=[dbc.themes.LUX])
navbar = dbc.Nav(className="nav nav-pills", children=[
    dbc.NavItem(html.Div('Covid-19 Tracker'), style={'font-size':'300%'}),
    dbc.NavItem(dbc.NavLink('Home', href="/"), style={'font-size':'200%'}, className="ml-auto mr-sm-2"),
    dbc.NavItem(dbc.NavLink('Trending', href="/Trending"), style={'font-size':'200%'}, className="my-2 my-sm-0")

])
server = app.server
app.title = 'Covid-19 India'
inputs = dbc.FormGroup([
    html.H4("Select State"),
    dcc.Dropdown(id="state", options=[{"label":x,"value":x} for x in statelist], value="INDIA",clearable=False)
]) 
app.layout = dbc.Container(fluid=True,children=[
		navbar,
    html.Br(),html.Br(),html.Br(),
    
    # html.Link(rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>),
    dbc.Row([
        dbc.Col(lg=3,md=2, children=[
            inputs, 
            html.Br(),html.Br(),html.Br(),
            html.Div(id="output-panel")
        ]),
    	dbc.Col(lg=3,md=2,children=[
    		html.Div(id="dist-panel")
    		], style={'width':'70%'}),
        dbc.Col(width={"offset": 3}, lg=3,md=2,children=[
            html.Div(dcc.Graph(id="state-pie")),
        ]),
        

    ])
])
@app.callback(dash.dependencies.Output('state-pie', 'figure'), inputs=[Input("state","value")])
def state_pie(state):
    return func.state_pie(state,todos)
@app.callback(output=Output("output-panel","children"), inputs=[Input("state","value")])
def render_output_panel(state):
	return func.disp_panel(state,todos)
stateresponse = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
dist = json.loads(stateresponse.text)
@app.callback(output=Output("dist-panel","children"), inputs=[Input("state","value")])
def output_panel(state):
	if(state=='INDIA'):
		return func.state_table(todos)
	else:
		return func.dist_table(dist,state)
if __name__ == '__main__':
    app.run_server(debug=True)
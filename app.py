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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,"assets")

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)

statelist=[]
todos['statewise'][0]['state']='INDIA'
for i in range(0,len(todos['statewise'])):
	statelist.append(todos['statewise'][i]['state'])
app = dash.Dash(assets_folder=STATIC_DIR)
navbar = html.Nav(className="navbar navbar-expand-lg navbar-light bg-light justify-content-between", children=[
    html.A(className="navbar-brand",children=['Covid-19 Tracker'], href='#', style={'font-size':'200%'}),
    html.Button(className="navbar-toggler", **{"data-toggle":"collapse"}, **{"data-target":"#navbarNavDropdown"}, **{"aria-expanded":"false"}, 
        **{"aria-controls":"navbarNavDropdown"}, **{"aria-label":"Toggle navigation"}, children=[
        html.Span(className="navbar-toggler-icon"),
        ]),
    html.Div(className="collapse navbar-collapse", **{"id":"navbarNavDropdown"}, children=[
        html.Ul(className="navbar-nav ml-auto",children=[
            html.Li(className='nav-item active', children=[
                html.A("Home",className='nav-link', href="#")], style={'font-size':'150%'}),
            html.Li(className='nav-item', children=[
                html.A("Trending",className='nav-link', href="#")], style={'font-size':'150%'}),
            ])
        ]),
    ])
app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
server = app.server
app.title = 'Covid-19 India'
inputs = html.Form([
    html.H4("Select State"),
    dcc.Dropdown(id="state", options=[{"label":x,"value":x} for x in statelist], value="INDIA",clearable=False)
])
app.layout = html.Div(className='container',children=[
		navbar,
        html.Br(),
        html.Div(id="time-panel"),
        html.Br(),
    html.Div(className='row',children=[
        html.Div(className='col-lg-3 col-md-3 col-sm-12', children=[
            inputs, 
            html.Br(),
            html.Br(),
            html.Div(id="output-panel"),
            html.Br(),
            html.P(className='alert alert-info',children=[
                html.P("Source: "),
                html.A("api.covid19india.org",href="api.covid19india.org"),
                ]),
            
        ]),
    	html.Div(className='col-lg-3 col-md-3 col-sm-12',children=[html.Div(className='table-responsive-sm',children=[
    		html.Div(id="dist-panel")]),
    		]),
        html.Div(className='offset-3 col-lg-3 col-md-3 col-sm-12',children=[
                html.Div(dcc.Graph(id="state-pie", responsive=True))
                ]),
        

    ])
])
@app.callback(output=Output("time-panel","children"), inputs=[Input("state","value")])
def state_pie(state):
    return func.last_updated(state)
@app.callback(dash.dependencies.Output('state-pie', 'figure'), inputs=[Input("state","value")])
def state_pie(state):
    return func.state_pie(state)
@app.callback(output=Output("output-panel","children"), inputs=[Input("state","value")])
def render_output_panel(state):
	return func.disp_panel(state)
stateresponse = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
dist = json.loads(stateresponse.text)
@app.callback(output=Output("dist-panel","children"), inputs=[Input("state","value")])
def output_panel(state):
	if(state=='INDIA'):
		return func.state_table()
	else:
		return func.dist_table(dist,state)
if __name__ == '__main__':
    app.run_server(debug=True)
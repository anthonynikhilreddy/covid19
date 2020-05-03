import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import requests
import os

from func.func import func

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,"static")

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
inputs = dbc.FormGroup([
    html.H4("Select State"),
    dcc.Dropdown(id="state", options=[{"label":x,"value":x} for x in statelist], value="INDIA",clearable=False)
]) 
app.layout = dbc.Container(fluid=True,children=[
		navbar,
    html.Br(),html.Br(),html.Br(),
    dbc.Row([
        dbc.Col(md=3, children=[
            inputs, 
            html.Br(),html.Br(),html.Br(),
            html.Div(id="output-panel")
        ]),
    	dbc.Col(md=3,children=[
    		html.Div(id="dist-panel")
    		])
    ])
])
@app.callback(output=Output("output-panel","children"), inputs=[Input("state","value")])
def render_output_panel(state):
	return func.disp_panel(state,todos)
	# return panel
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
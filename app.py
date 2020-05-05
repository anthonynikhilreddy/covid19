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
STATIC_DIR = os.path.join(BASE_DIR,"assets")

## external scripts
external_scripts = [
    {
      "src":"https://code.jquery.com/jquery-3.4.1.slim.min.js",
      "integrity":"sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n",
      "crossorigin":"anonymous"
    },
    {
        "src":"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
        "integrity":"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6",
        "crossorigi":"anonymous"
    },
    {
    "src":"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
    "integrity":"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo",
    "crossorigin":"anonymous"
    }

]
## external stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    },
]

## creating the dash object
app = dash.Dash(__name__,assets_folder=STATIC_DIR,
            external_scripts=external_scripts,
            external_stylesheets=external_stylesheets,
            meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

server=app.server

app.title = 'Covid-19 India'
navbar = html.Nav(className="navbar navbar-expand-lg navbar-light bg-light justify-content-between", children=[
    html.A(className="navbar-brand",children=['Covid-19 Tracker'], href='#', style={'font-size':'200%'}),
        html.Ul(className="navbar-nav ml-auto",children=[
            html.Li(className='d-none d-md-block nav-item active', children=[
                html.A(children=[html.H3("Spring Boot Version"),html.H6("By Abhinav")],className='nav-link', href="https://knowcovid19india.herokuapp.com/")], style={'font-size':'150%'}),
            ])
    ])

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)
statelist=[]
todos['statewise'][0]['state']='INDIA'
for i in range(1,len(todos['statewise'])):
    statelist.append(todos['statewise'][i]['state'])
statelist.sort()
inputs = html.Form([
    html.H4("Select State"),
    dcc.Dropdown(id="state", options=[{"label":x,"value":x} for x in statelist], value="INDIA",clearable=False)
])
app.layout = html.Div([
    html.Div(className='container-fluid',children=[
        navbar,
        html.Br(),
        html.Div(id="time-panel"),
    html.Div(className='row',children=[
        html.Div(className='col-lg-3 col-md-3 col-sm-12', children=[
            inputs, 
            html.Br(),
            html.Br(),
            html.Div(id="output-panel"),
            html.Br(),
            html.Div(id="news-panel"),
            ]),
        html.Div(className='col-lg-6 col-md-3 col-sm-12',children=[html.Div(className='table-responsive-sm',children=[
            html.Div(id="dist-panel")], style={'border-radius':'2px'}),
            html.Div(className="row alert",children=[
                html.Div(children=[
                html.P(children=[
                    html.P(children=[
                        html.Div(children=["Made with ",html.Span("\u2665",style={"color":"red"})," by ",html.A("Anthony",href="https://www.linkedin.com/in/anthonynikhilreddy/",style={'color':'black',"font-weight":"bold"})]),
                        html.Br(),
                        html.P(children=["Source: ",html.A("api.covid19india.org",href="https://api.covid19india.org")]),
                        ]),
                        ])
                ])
            ],style={"width":"90%","margin-left":"4px","background-color":"#F8F9FA"})
            ],

            ),
        html.Div(className='d-none d-md-block col-lg-3 col-md-3 col-sm-12',children=[
                html.Div(dcc.Graph(id="state-pie", responsive=True)),
                ]),
    ]),

    ])
])
@app.callback(output=Output("news-panel","children"), inputs=[Input("state","value")])
def news(state):
    return func.news_panel(state)
@app.callback(output=Output("time-panel","children"), inputs=[Input("state","value")])
def last_updated(state):
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
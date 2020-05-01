import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import requests
import dash_table

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)
l=['State/UT','Confirmed','Active','Deceased','Recovered']
def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(_) for _ in l])
        ),
        html.Tbody([
            html.Tr([
                html.Td(todos['statewise'][i]['state']),
                html.Td([
                    todos['statewise'][i]['confirmed'],
                    html.P(children='\u2191'+todos['statewise'][i]['deltaconfirmed'], style={'font-size': '20%', 'color':'red'}),
                    ]),
                html.Td([
                    todos['statewise'][i]['active'],
                    ]),
                html.Td([todos['statewise'][i]['deaths'],
                    html.P(children='\u2191'+todos['statewise'][i]['deltadeaths'], style={'font-size': '20%', 'color':'grey'})
                    ]),
                html.Td([todos['statewise'][i]['recovered'],
                    html.P(children='\u2191'+todos['statewise'][i]['deltarecovered'], style={'font-size': '20%', 'color':'green'})
                    ]),

            ]) for i in range(1,len(todos['statewise']))
        ])
    ], style={'width':'50%', 'textAlign': 'center'})


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='covid19india'),
    generate_table(todos)
])

if __name__ == '__main__':
    app.run_server(debug=True)
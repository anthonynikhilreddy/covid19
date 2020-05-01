import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import requests

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)

l=['State/UT','Active','Deceased','Recovered']
def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(_) for _ in l])
        ),
        html.Tbody([
            html.Tr([
                html.Td(todos['statewise'][i]['state']),
                html.Td([
                    todos['statewise'][i]['active'],
                    html.Sub(todos['statewise'][i]['deltaconfirmed'])
                    ]),
                html.Td(todos['statewise'][i]['deaths']),
                html.Td(todos['statewise'][i]['recovered']),

            ]) for i in range(1,len(todos['statewise']))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='covid19india'),
    # html.P(children=(todos)),
    generate_table(todos)
])

if __name__ == '__main__':
    app.run_server(debug=True)
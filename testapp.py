import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html



df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')

df=df[1:]

processe_Df = df[['State', 'Confirmed', 'Deaths', 'Recovered']].copy()

# l=['State/UT','Active','Deceased','Recovered']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
	html.H1(children='Covid-19 India Statistics'),
	dash_table.DataTable(
    id='table',
    data=df.to_dict("rows"),
    columns=[{"name": i, "id": i} for i in processe_Df.columns],
    style_as_list_view=True,
    style_cell={
    	'padding': '5px',
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'overflow':'hidden',
    },
    style_cell_conditional=[
        {
            'if': {'column_id': 'State'},
            'textAlign': 'left'
        },
        {
        	'if': {'column_id': 'State'},
        	'maxWidth': '50px'
        },
        {
            'if': {'column_id': 'Confirmed'},
            'maxWidth': '30px',
        },
        {
            'if': {'column_id': 'Deaths'},
            'maxWidth': '30px',
        },
        {
            'if': {'column_id': 'Recovered'},
            'maxWidth': '30px',
        }
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
)
], style={'width':'50%', 'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True)
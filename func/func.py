import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import requests
import dash_table
from shapely.geometry import Point, Polygon
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
colors = ['#007BFF','red','green']
qqq=['District','Confirmed','Active','Deceased','Recovered']
l=['State/UT','Confirmed','Active','Deceased','Recovered']
statelist=[]
# todos['statewise'][0]['state']='INDIA'
response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)
for i in range(1,len(todos['statewise'])):
	statelist.append(todos['statewise'][i]['state'])
class func:
	def __init__(self):
		a="hello"
	def state_table(todos):
		rows=[]
		for i in range(1,len(todos['statewise'])):
			row=[]
			row1=[]
			row2=[]
			row3=[]
			row4=[]
			row5=[]
			row1.append(html.Td(todos['statewise'][i]['state']))
			if(todos['statewise'][i]['deltaconfirmed']!='0'):
				row2.append(html.Td([
					todos['statewise'][i]['confirmed'],
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltaconfirmed'], style={'font-size': '30%', 'color':'red', 'display':'inline'}),
					]))
			else:
				row2.append(html.Td(todos['statewise'][i]['confirmed']))
			row3.append(html.Td(todos['statewise'][i]['active']))
			if((todos['statewise'][i]['deltadeaths'])!='0'):
				row4.append(html.Td([
					todos['statewise'][i]['deaths'],
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltadeaths'], style={'font-size': '30%', 'color':'gray', 'display':'inline'}),
					]))
			else:
				row4.append(html.Td(todos['statewise'][i]['deaths']))
			if(todos['statewise'][i]['deltarecovered']!='0'):
				row5.append(html.Td([
					todos['statewise'][i]['recovered'],
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltarecovered'], style={'font-size': '30%', 'color':'green', 'display':'inline'}),
					]))
			else:
				row5.append(html.Td(todos['statewise'][i]['recovered']))
			row=row1+row2+row3+row4+row5
			rows.append(html.Tr(row,style={'font-size':'150%'}))
		
		panel = html.Div(children=[html.H4("INDIA"),html.Div([dbc.Table([html.Thead(html.Tr([html.Th(_) for _ in l]))] + (rows), bordered=True)])])
		return panel

	def dist_table(dist,state):
		rows=[]
		for _ in range(len(dist)):
			if(dist[_]['state']==state):
				for i in range(len(dist[_]['districtData'])):
					row=[]
					row1=[]
					row2=[]
					row3=[]
					row4=[]
					row5=[]
					row1.append(html.Td(dist[_]['districtData'][i]['district']))
					if(dist[_]['districtData'][i]['delta']['confirmed']!=0):
						row2.append(
							html.Td([
								dist[_]['districtData'][i]['confirmed'],
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['confirmed']), style={'font-size': '30%', 'color':'red', 'display':'inline'}),
								]))
					else:
						row2.append(html.Td(dist[_]['districtData'][i]['confirmed']))
					row3.append(html.Td(dist[_]['districtData'][i]['active']))
					if((dist[_]['districtData'][i]['delta']['deceased'])!=0):
						row4.append(
							html.Td([
								dist[_]['districtData'][i]['deceased'],
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['deceased']), style={'font-size': '30%', 'color':'gray', 'display':'inline'}),
								]))
					else:
						row4.append(html.Td(dist[_]['districtData'][i]['deceased']))
					if(dist[_]['districtData'][i]['delta']['recovered']!=0):
						row5.append(
							html.Td([
								dist[_]['districtData'][i]['recovered'],
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['recovered']), style={'font-size': '30%', 'color':'green', 'display':'inline'}),
								]))
					else:
						row5.append(html.Td(dist[_]['districtData'][i]['recovered']))
					row=row1+row2+row3+row4+row5
					rows.append(html.Tr(row,style={'font-size':'150%'}))
				break
		panel = html.Div(children=[html.H4(state),html.Div([dbc.Table([html.Thead(html.Tr([html.Th(_) for _ in qqq]),style={'font-size':'200%', 'color':'red'})] + (rows), bordered=True)])], style={'width':'70%'})
		return panel
	def disp_panel(state,todos):
		total_cases_until_today=(todos['statewise'][0]['confirmed'])
		active_cases_until_today=(todos['statewise'][0]['active'])
		deaths_until_today=(todos['statewise'][0]['deaths'])
		recovered_until_today=(todos['statewise'][0]['recovered'])
		for i in range(1,len(todos['statewise'])):
			if(todos['statewise'][i]['state']==state):
				total_cases_until_today=(todos['statewise'][i]['confirmed'])
				active_cases_until_today=(todos['statewise'][i]['active'])
				deaths_until_today=(todos['statewise'][i]['deaths'])
				recovered_until_today=(todos['statewise'][i]['recovered'])
				break
		panel = html.Div([
			html.H4(state),
	        dbc.Card(body=True, className="text-white bg-primary", children=[
	            html.H6("Total cases until today:", style={"color":"white"}),
	            html.H3(total_cases_until_today, style={"color":"white"}),
	            html.H6("Active cases until today:", className="text-danger"),
	            html.H3(active_cases_until_today, className="text-danger"),
	            html.H6("Deaths until today:", style={"color":"gray"}),
	            html.H3(deaths_until_today, style={"color":"gray"}),
	            html.H6("Recovries until today:", style={"color":"green"}),
	            html.H3(recovered_until_today, style={"color":"green"}),
	        ])
	        ])
		return panel
	def state_pie(state,todos):
		fig = go.Figure(data=[go.Pie(labels=['Active','Deceased','Recovered'],
		                             values=[todos['statewise'][0]['active'],todos['statewise'][0]['deaths'],
		                             todos['statewise'][0]['recovered']],hole=.3)])
		fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
		                  marker=dict(colors=colors,line=dict(color='#000000', width=2)))
		fig.update_layout(title_text='INDIA')
		for i in range(1,len(todos['statewise'])):
			if(todos['statewise'][i]['state']==state):
				fig = go.Figure(data=[go.Pie(labels=['Active','Deceased','Recovered'],
		                             values=[todos['statewise'][i]['active'],todos['statewise'][i]['deaths'],
		                             todos['statewise'][i]['recovered']],hole=.3)])
				fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
		                  marker=dict(colors=colors,line=dict(color='#000000', width=2)))
				fig.update_layout(title_text=state)
		return fig
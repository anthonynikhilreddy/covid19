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
url = ('http://newsapi.org/v2/top-headlines?country=in&q=corona&apiKey=4392327483d240b98d82f709d314b7a1')
news = requests.get(url)
newsresponse=news.json()
class func:
	def __init__(self):
		a="hello"
	def last_updated(state):
		todos['statewise'][0]['state']='INDIA'
		for i in range(0,len(todos['statewise'])):
			if(todos['statewise'][i]['state']==state):
				s=""
				if(int(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[0])==0):
					s=s+"12:"+str(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[1])+"AM"
				elif(int(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[0])<12):
					s=s+str(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[1])+ \
					str(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[1])+"AM"
				elif(int(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[0])==12):
					s=s+"12:"+str(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[1])+"PM"
				elif(int(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[0])>12):
					s=s+str(int(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[0])-12)+":"+ \
					str(todos['statewise'][i]['lastupdatedtime'].split(' ')[1].split(':')[1])+"PM"
				return html.P(className="alert alert-primary",**{"role":"alert"}, children=["Last updated on "+todos['statewise'][i]['lastupdatedtime'].split(' ')[0]+" at "+s], style={"textAlign":"center","font-size":"120%"})
	def state_table():
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
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltaconfirmed'], style={'font-size': '70%', 'color':'red', 'display':'inline'}),
					]))
			else:
				row2.append(html.Td(todos['statewise'][i]['confirmed']))
			row3.append(html.Td(todos['statewise'][i]['active']))
			if((todos['statewise'][i]['deltadeaths'])!='0'):
				row4.append(html.Td([
					todos['statewise'][i]['deaths'],
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltadeaths'], style={'font-size': '70%', 'color':'gray', 'display':'inline'}),
					]))
			else:
				row4.append(html.Td(todos['statewise'][i]['deaths']))
			if(todos['statewise'][i]['deltarecovered']!='0'):
				row5.append(html.Td([
					todos['statewise'][i]['recovered'],
					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltarecovered'], style={'font-size': '70%', 'color':'green', 'display':'inline'}),
					]))
			else:
				row5.append(html.Td(todos['statewise'][i]['recovered']))
			row=row1+row2+row3+row4+row5
			if(i%2!=0):
				rows.append(html.Tr(row,style={'background-color':'#F1F1F1'}))
			else:
				rows.append(html.Tr(row))
		panel = html.Div(children=[html.H4("INDIA"),html.Div([dbc.Table([html.Thead(html.Tr([html.Th(_) for _ in l]))] + (rows), style={'border-collapse':'collapse', 'overflow':'auto', "border":"none"})])], style={"width":"90%"})
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
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['confirmed']), style={'font-size': '70%', 'color':'red', 'display':'inline'}),
								]))
					else:
						row2.append(html.Td(dist[_]['districtData'][i]['confirmed']))
					row3.append(html.Td(dist[_]['districtData'][i]['active']))
					if((dist[_]['districtData'][i]['delta']['deceased'])!=0):
						row4.append(
							html.Td([
								dist[_]['districtData'][i]['deceased'],
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['deceased']), style={'font-size': '70%', 'color':'gray', 'display':'inline'}),
								]))
					else:
						row4.append(html.Td(dist[_]['districtData'][i]['deceased']))
					if(dist[_]['districtData'][i]['delta']['recovered']!=0):
						row5.append(
							html.Td([
								dist[_]['districtData'][i]['recovered'],
								html.P(children='\u0020'+'\u0020'+'\u2191'+str(dist[_]['districtData'][i]['delta']['recovered']), style={'font-size': '70%', 'color':'green', 'display':'inline'}),
								]))
					else:
						row5.append(html.Td(dist[_]['districtData'][i]['recovered']))
					row=row1+row2+row3+row4+row5
					if(i%2!=0):
						rows.append(html.Tr(row,style={'background-color':'#F1F1F1'}))
					else:
						rows.append(html.Tr(row))
				break
		panel = html.Div(children=[html.H4(state),html.Div([dbc.Table([html.Thead(html.Tr([html.Th(_) for _ in qqq]))] + (rows), style={'border-collapse':'collapse', 'overflow':'auto', "border":"none"})])],style={"width":"90%"})
		return panel
	def disp_panel(state):
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
	        dbc.Card(body=True, children=[
	            html.H6("Total cases until today:", style={"color":"white"}),
	            html.H3(total_cases_until_today, style={"color":"white"}),
	            html.H6("Active cases until today:", className="text-danger"),
	            html.H3(active_cases_until_today, className="text-danger"),
	            html.H6("Deaths until today:", style={"color":"gray"}),
	            html.H3(deaths_until_today, style={"color":"gray"}),
	            html.H6("Recovries until today:", style={"color":"green"}),
	            html.H3(recovered_until_today, style={"color":"green"}),
	        ], style={'background-color': 'black'})
	        ])
		return panel
	def news_panel(state):
		newstitles=[]
		newsurls=[]
		newssources=[]
		news=[]
		for i in range(len(newsresponse['articles'])):
			news.append(html.Tr(children=[
				# html.Button(newsresponse['articles'][i]['title'].split('-')[0],**{"onclick":newsresponse['articles'][i]['url']}),
				html.A(newsresponse['articles'][i]['title'],href=newsresponse['articles'][i]['url']),
				# html.A(newsresponse['articles'][i]['title'].split('-')[0],href=newsresponse['articles'][i]['url']),
				html.Br(),

				html.Br()
				])
			)
		panel = html.Div(className='alert alert-primary',children=[
			# html.Div(children=[html.H4(state[0].upper()+state[1:].lower()+" News")]),
			html.Div(children=[html.H4("News")]),
			html.Div(news)])
		return panel
	def state_pie(state):
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
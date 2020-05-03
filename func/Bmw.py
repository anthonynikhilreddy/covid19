# class func:
# 	def __init__(self):
# 		a="hello"
# 	def generate_table(todos):
# 		rows=[]
# 		for i in range(1,len(todos['statewise'])):
# 			row=[]
# 			row1=[]
# 			row2=[]
# 			row3=[]
# 			row4=[]
# 			row5=[]
# 			row1.append(html.Td(todos['statewise'][i]['state']))
# 			if(todos['statewise'][i]['deltaconfirmed']!='0'):
# 				row2.append(html.Td([
# 					todos['statewise'][i]['confirmed'],
# 					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltaconfirmed'], style={'font-size': '20%', 'color':'red', 'display':'inline'}),
# 					]))
# 			else:
# 				row2.append(html.Td(todos['statewise'][i]['confirmed']))
# 			row3.append(html.Td(todos['statewise'][i]['active']))
# 			if((todos['statewise'][i]['deltadeaths'])!='0'):
# 				row4.append(html.Td([
# 					todos['statewise'][i]['deaths'],
# 					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltadeaths'], style={'font-size': '20%', 'color':'gray', 'display':'inline'}),
# 					]))
# 			else:
# 				row4.append(html.Td(todos['statewise'][i]['deaths']))
# 			if(todos['statewise'][i]['deltarecovered']!='0'):
# 				row5.append(html.Td([
# 					todos['statewise'][i]['recovered'],
# 					html.P(children='\u0020'+'\u0020'+'\u2191'+todos['statewise'][i]['deltarecovered'], style={'font-size': '20%', 'color':'green', 'display':'inline'}),
# 					]))
# 			else:
# 				row5.append(html.Td(todos['statewise'][i]['recovered']))
# 			row=row1+row2+row3+row4+row5
# 			rows.append(html.Tr(row))
# 		return dbc.Table([html.Thead(html.Tr([html.Th(_) for _ in l]))] + (rows), bordered=True)
class Bmw: 
    # First we create a constructor for this class 
    # and add members to it, here models 
    def __init__(self): 
        self.models = ['i8', 'x1', 'x5', 'x6'] 
   
    # A normal print function 
    def outModels(self): 
        print('These are the available models for BMW') 
        for model in self.models: 
            return('\t%s ' % model) 
import json
import requests

response = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
dist = json.loads(response.text)
# response = requests.get("https://api.covid19india.org/data.json")
# todos = json.loads(response.text)
for _ in range(len(dist)):
	print(dist[_]['state'])
	for i in range(len(dist[_]['districtData'])):
		print(dist[_]['districtData'][i])
# dist['statewise'][0]['state']='india'
# print(dist['statewise'][0]['state'])
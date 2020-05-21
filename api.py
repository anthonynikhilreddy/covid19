import json
import requests
response = requests.get("https://api.covid19india.org/state_test_data.json")
todos = json.loads(response.text)
# todos['statewise'][0]['lastupdatedtime'].split(' ')[1].split(':')[0]='23'
# for i in range(len(todos['tested'])):
# print(todos['states_tested_data'][7])
# print(len(todos['states_tested_data']))
# for i in range(0,len(todos['states_tested_data']),3):
print(todos['states_tested_data'][60])
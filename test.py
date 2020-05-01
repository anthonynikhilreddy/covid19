import json
import requests

response = requests.get("https://api.covid19india.org/data.json")
todos = json.loads(response.text)
print(todos['statewise'][5])
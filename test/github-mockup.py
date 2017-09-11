import json
import requests

with open('hook-sample.json') as data_file:
    data = json.load(data_file)
    
headers = {'Content-type': 'application/json'}

r = requests.post("http://localhost:8000/pyload", data=json.dumps(data), headers=headers)

print r.text

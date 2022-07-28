import csv
import requests
import json

header = {'Accept': 'application/json', 'Content-Type': 'application/json'}

with open ("csv_files/netflix_titles.csv", encoding='utf-8') as file:
    csv_file = csv.DictReader(file)
    
    for row in csv_file:
        jsonArray = []
        jsonArray.append(row)
        show_id=row['show_id']
        jsonString = json.dumps(jsonArray[0])
        print (jsonString)
        req1 = requests.post("http://127.0.0.1:8080/titles", data=jsonString, headers=header)
        print (req1)

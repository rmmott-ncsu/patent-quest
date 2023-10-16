import json
import pandas as pd

with open('patents_2013.json', 'r') as file:
    data = json.load(file)
    file.close()

df = pd.json_normalize(data['patents'])
print(df)
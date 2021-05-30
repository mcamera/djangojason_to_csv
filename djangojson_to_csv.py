import pandas as pd
import json
import os
import sys

# Checking if the path was informed as arg
try:
    path= sys.argv[1]
except IndexError:
    raise SystemExit(f"ERROR! Usage: {sys.argv[0]} /<path_where_the_jsons_are>/")

# Checking if the path exists
try:
    os.listdir(path)
except FileNotFoundError:
    raise SystemExit(f"ERROR! No such file or directory:", path)

# This will list all json files and put in a list
json_files =[]
for file in os.listdir(path):
    if file.endswith('.json'):
        json_files.append(path + file)

# Convert .json to .csv for each file in a directory:
for json_file in json_files:
    try:
        with open(json_file,'r', encoding="latin1") as f:
            data = json.loads(f.read())

        df = pd.json_normalize(data) # flattening the json
        df.drop(['model'], axis=1, inplace=True) # this column is not important
        df.rename(columns={"pk": "id"}, inplace=True) #the 'pk' is our 'id'

        for i in df.columns:
            if i.startswith('fields'):
                df.rename(columns={i:i[7:]}, inplace=True) # this will remove the 'fields.' from the column name
        
        csv_file = json_file[:-5] + '.csv' # change the .json to .csv
        df.to_csv(csv_file, encoding="latin1", index=False) # save to csv
        
        print('The file', json_file, 'was converted to:', csv_file)

    except FileNotFoundError:
        raise SystemExit(f"ERROR! No such file or directory:", json_file)
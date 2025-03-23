import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd 
import re
import json
from cores.utils import filter_json_markdown

df = pd.read_csv('data_baseline_v4/baseline_v4.csv')


GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""


value_df = pd.DataFrame(columns=['system', 'user', 'json']) 
for idx, row in df.iterrows():
    json_c = row['json']
    user = row['user']
    # remove Note that today is ... in user prompt
    user = re.sub(r'Note that today is .*', '', user)
    # remove \n from user columns from the last character
    user = user.rstrip('\n')
    
    system =GEN_VALUE_SYSTEM_WITHOUT_EXM
    
    try: 
        # if json is string can convert to int, then it is value
        json_c = int(json_c)
        
        # add row to value_df
        value_df = pd.concat([value_df, df.iloc[[idx]]], ignore_index=True)
    except: 
        # json_c is an json object 
        match = filter_json_markdown(json_c)
        if match:
            
            try:
                json_data = json.loads(match)
                if 'value' in json_data:
                    # add row to value_df with new system and user, value 
                    value_df = value_df._append(pd.DataFrame({
                        'system': [system],
                        'user': [user],
                        'json': [json_data['value']]
                    }))
                    
                    
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
# remove duplicate lines
value_df = value_df.drop_duplicates()
# remove empty lines
value_df = value_df.dropna()



# remove \n from user columns 
value_df['user'] = value_df['user'].str.replace('\n', '')
# check if the last character of system is \n then remove the last character
value_df['system'] = value_df['system'].str.rstrip('\n')

user = value_df.iloc[[0]]['user']
print(user.values)
value_df.to_csv('data_baseline_v4/value_data_v2.csv', index=False, encoding='utf-8')
print(value_df.head())
print(value_df.info())
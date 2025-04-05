import pandas as pd
import json
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cores.utils import filter_json_markdown
from tqdm import tqdm
import re 
from cores.schema.cashbox import CashFlowInformation
from cores.output_parser.vi_pydantic import ViPydanticOutputParser


output_parser = ViPydanticOutputParser(CashFlowInformation) 
output_str = output_parser.format_string 

system_str = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user"""

system_str = f"{system_str}\n{output_str}"

path = 'data/data_baseline_v7/baseline_v7_fix_value.csv'
df = pd.read_csv(path)



new_df = pd.DataFrame(columns=['system', 'user', 'json'])

# Iterate through the rows of the original DataFrame
for index, row in df.iterrows():
    try:
        # Convert the value in the 'json' column to a dictionary
        json_str = row['json']
        # Remove the markdown formatting
        json_str_filter = filter_json_markdown(json_str)
        # Load the JSON string into a dictionary
        json_value = json.loads(json_str_filter)
        
        value = int(float(str(json_value['value'])))
        
        json_value['value'] = value
        
        json_str_fix_value = json.dumps(json_value, indent=4, ensure_ascii=False)
        
        new_df = new_df._append({
            'system': system_str, 
            'user': row['user'],
            'json': f"""```json\n{json_str_fix_value}\n```""",
        }, ignore_index=True)

    except (ValueError, TypeError, json.JSONDecodeError) as e:
        print(e)
        # Handle cases where the 'json' column value is invalid
        print(f"Invalid JSON in row {index}: {row['json']}")

    

new_df.to_csv('data/data_baseline_v7/baseline_v7_fix_value_new.csv', index=False, encoding='utf-8')
# print(new_df)

import pandas as pd
import json
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
from openai import OpenAI
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, GEN_FORMAT_USER_STR, DAY_MAPPING, EXAMPLE
from cores.utils import filter_json_markdown_anywhere, filter_json_markdown
from tqdm import tqdm
import re 


SYSTEM_MSG = """You are a money manager assistant.
Your job is to extract time information in JSON from provided sentence.

Here's a JSON schema to follow:
{{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to mentioned day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
"""

client = OpenAI(
    base_url="http://10.0.4.239:8016/v1",
    api_key="emansieuvc"
)

model_name = '/qwen-reasoning-time-full-dataset-v1'

def predict_time(user_prompt): 
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )
    raw_context = response.choices[0].message.content
    context = filter_json_markdown_anywhere(raw_context)
    context = context.replace('{{', '{').replace('}}', '}')
    
    # remove double "" in context
    context = re.sub(r'\"\"', '"', context)

    return context, raw_context
  
  
df = pd.read_csv('data/data_baseline_v8/baseline_v8_category_random.csv') 
acc = []
for idx, row in tqdm(df.iterrows(), total=len(df)):
    try:
        context, raw_context = predict_time(row['user'])
        predicted_time = json.loads(context)
        labeled_json = json.loads(filter_json_markdown(row['json']))
        labeled_time = labeled_json['when']
        
        if predicted_time != labeled_time:
            print(f"========================")
            print(f"User row {idx}: {row['user']}") 
            print(f"Predicted: {predicted_time}")
            print(f"Labeled: {labeled_time}")
            print(f"Raw context:\n {raw_context}\n\n")
            acc.append(0) 
        else: 
            acc.append(1)
            
    except json.JSONDecodeError as e:
        print(f"======================== row : {idx}")
        print(f"JSONDecodeError: {e}\n\n")
        continue

print(f"Accuracy over {len(acc)}: {sum(acc) / len(acc)}")
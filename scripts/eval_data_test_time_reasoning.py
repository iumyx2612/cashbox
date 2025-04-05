import pandas as pd
import json
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
from openai import OpenAI
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, GEN_FORMAT_USER_STR, DAY_MAPPING, EXAMPLE
from cores.utils import filter_json_markdown_anywhere
from tqdm import tqdm
import re 


SYSTEM_MSG = """You are a money manager assistant.
Your job is to extract time information in JSON from provided sentence.

Here's a JSON schema to follow:
{{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to mentioned day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
"""

# client = OpenAI(
#     base_url="http://10.0.4.239:8010/v1",
#     api_key="emansieuvc"
# )

client = OpenAI(
    base_url="http://10.0.7.50:8011/v1",
    api_key="emansieuvc"
)

model_name = '/qwen-reasoning-time-full-dataset-v1'

def predict_time(sentence: str,day: str): 
    user_prompt = GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)
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

df = pd.read_excel('data/data_test/data_test_time.xlsx')

acc = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try: 
        if index == 17: 
            print(row['Example'])
            continue
        # Task all
        sentence = row['Example']
        relative_time = int(row['Time'])
        ab_time = str(row['real-time']).replace('"', '') if str(row['real-time']) != 'nan' else None
        day = int(float(str(row['Today']))) - 2
        day = DAY_MAPPING[day]
        time_str, context = predict_time(sentence, day)
        time_dict = json.loads(time_str)
        relative_date = time_dict['relative_date']
        absolute_date = time_dict['absolute_date']
        
        if ab_time is None: 
            if int(relative_time) != int(relative_date):
                acc.append(0)
                print("\n\n\n-------------------------------")
                print(f"Erorr with ab_time is None :: {sentence},Note that to day is {day}, True value relative_time: {relative_time}, True value ab_time : {ab_time} - \n\ncontext: \n{context}")
            else:
                acc.append(1)
        else: 
            if int(relative_time) != int(relative_date) or ab_time != absolute_date:
                acc.append(0)
                print("\n\n\n-------------------------------")
                print(f"Erorr with ab_time is {ab_time} :: {sentence},Note that to day is {day}, True value relative_time: {relative_time}, True value ab_time : {ab_time} - \n\ncontext: \n{context}")
            else:
                acc.append(1)
        
        # df.at[index, 'output'] = int_output
    except Exception as e:
        print(e)

# df.to_excel('data/data_test/data_test_output_model-v7.xlsx', index=False, engine='xlsxwriter')  

if len(acc) > 0:
    print("Mean: ", sum(acc)/len(acc))
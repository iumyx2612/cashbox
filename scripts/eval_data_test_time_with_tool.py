import json
import os
import pandas as pd
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / 'cores'))

from dotenv import load_dotenv
from tqdm import tqdm

from openai import OpenAI

from cores.schema.time_tool import calculate_time
from cores.prompts.time.time_function import TIME_FUNCTION_SYSTEM, TIME_FUNCTION_USER
from cores.prompts.gen_json import DAY_MAPPING
from cores.prompts.gen_json import GEN_FORMAT_USER_STR
from cores.utils import filter_json_markdown

TIME_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information

Tool schema:
{'type': 'function', 'function': {'name': 'calculate_time', 'description': 'calculate_time(today: Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], mentioned_date: Optional[Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật']] = None, week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today'], 'type': 'object'}}}
"""


client = OpenAI(
    base_url="http://10.0.7.50:8011/v1",
    api_key="emansieuvc"
)

model_name = '/qwen-baseline-time-function-calling-v2'

def predict_time(sentence: str,day: str): 
    user_prompt = GEN_FORMAT_USER_STR.format(
        sentence=sentence,
        day=day
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": TIME_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0,
    )
    
    time_str = response.choices[0].message.content
    time_dict = json.loads(filter_json_markdown(time_str)) 
    time_value_from_tool = calculate_time(**time_dict)
    return time_value_from_tool, time_str



df = pd.read_excel('data/data_test/data_test_time_v2.xlsx')

acc = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try: 
        # Task all
        sentence = row['Example']
        relative_time = row['Time']
        ab_time = str(row['real-time']).replace('"', '') if str(row['real-time']) != 'nan' else None
        day = int(float(str(row['Today']))) - 2
        day = DAY_MAPPING[day]
        time_dict, time_str = predict_time(sentence, day)
        relative_date = time_dict['relative_date']
        absolute_date = time_dict['absolute_date']
        
        if ab_time is None: 
            if int(relative_time) != int(relative_date):
                acc.append(0)
                print("\n\n\n-------------------------------")
                print(f'Sentence : {sentence}, today : {day}')
                print(f"Label relative_time: {relative_time}, label ab_time : {ab_time}") 
                print(f"Predict relative_time: {relative_date}, predict ab_time : {absolute_date}")
                print(f"Tool call: \n {time_str}\n\n")
            else:
                acc.append(1)
        else: 
            if ab_time != absolute_date:
                acc.append(0)
                print("\n\n\n-------------------------------")
                print(f'Sentence : {sentence}, today : {day}')
                print(f"Label relative_time: {relative_time}, label ab_time : {ab_time}")
                print(f"Predict relative_time: {relative_date}, predict ab_time : {absolute_date}")
                print(f"Tool call: \n {time_str}\n\n")
                
            else:
                acc.append(1)
        
        # df.at[index, 'output'] = int_output
    except Exception as e:
        print(index, e)
    

# df.to_excel('data/data_test/data_test_output_model-v7.xlsx', index=False, engine='xlsxwriter')  

if len(acc) > 0:
    print("Mean: ", sum(acc)/len(acc))


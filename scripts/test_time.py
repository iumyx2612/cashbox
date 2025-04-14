import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / 'cores'))
import json
import pandas as pd
from cores.schema.time_tool import calculate_time

from openai import AsyncOpenAI
from cores.utils import filter_json_markdown
from tqdm import tqdm
import re 
import asyncio

FUNCTION_CALLING_TIME_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information

Tool schema:
{'type': 'function', 'function': {'name': 'calculate_time', 'description': 'calculate_time(today: Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], mentioned_date: Optional[Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật']] = None, week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today'], 'type': 'object'}}}
"""

model_name = '/qwen-time-function-calling-v3'

client = AsyncOpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc", 
)

async def predict_time(user_prompt): 
    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": FUNCTION_CALLING_TIME_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )
    raw_context = response.choices[0].message.content
    context = filter_json_markdown(raw_context)
    context = context.replace('{{', '{').replace('}}', '}')
    
    # remove double "" in context
    context = re.sub(r'\"\"', '"', context)
    context_dict = json.loads(context)
    value = calculate_time(**context_dict)
    
    return value
  
async def main():
    df = pd.read_csv('data/data_baseline_v8/baseline_v8_category.csv') 
    df = df.drop_duplicates(subset=['user'])
    new_df = pd.DataFrame(columns=df.columns)
    # for each row 
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try: 
            user = row['user']
            json_dict = json.loads(filter_json_markdown(row['json']))
            
            value = await predict_time(user)
            json_dict['when'] = value
            
            json_str = json.dumps(json_dict, ensure_ascii=False, indent=4)
            
            row['json'] = f"```json\n{json_str}\n```"
            new_df = new_df._append(row, ignore_index=True)
        except Exception as e:
            print(f"Error: {e}, index : {index}")
            continue


    new_df.to_csv('data/data_baseline_v9/baseline_v9_category_fix_time.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    asyncio.run(main())
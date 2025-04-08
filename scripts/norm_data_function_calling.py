import pandas as pd
from llama_index.core.output_parsers.utils import extract_json_str as filter_json_markdown
import json

path = 'data/time_reasoning/function_calling_v2.csv'

df = pd.read_csv(path)

DAY_ARRAY = [
    'Thứ hai', 
    'Thứ ba',
    'Thứ tư',
    'Thứ năm',
    'Thứ sáu',
    'Thứ bảy',
    'Chủ Nhật',
]
num_change = 0
for idx, row in df.iterrows():
    try:
        json_value = row['json']
        json_value = filter_json_markdown(json_value)
        json_dict = json.loads(json_value)
        
        today = json_dict['today']
        mentioned_date = json_dict['mentioned_date']
        
        # normalize today and mentioned_date to fit the DAY_ARRAY
        # low all the string and upper the first letter of the first word
        if today is not None:
            today = today[0].upper() + today[1:].lower()
            if today == 'Chủ nhật':
                today = 'Chủ Nhật'
        if mentioned_date is not None:
            mentioned_date = mentioned_date[0].upper() + mentioned_date[1:].lower()
            if mentioned_date == 'Chủ nhật':
                mentioned_date = 'Chủ Nhật'
        
        flag_change = False
        if mentioned_date is None: 
            continue
        else: 
            mentioned_array = DAY_ARRAY.index(mentioned_date)
            today_array = DAY_ARRAY.index(today)
            if mentioned_array > today_array and json_dict['week'] == 0: 
                json_dict['week'] = 1
                flag_change = True
        
        relation_date = json_dict['relative_date']
        if relation_date is not None and isinstance(relation_date, int): 
            json_dict['mentioned_date'] = None
            json_dict['week'] = 0
            flag_change = True
        
        abs_date = json_dict['absolute_date']
        if abs_date is not None and isinstance(abs_date, str): 
            json_dict['mentioned_date'] = None
            json_dict['relative_date'] = None
            json_dict['week'] = 0
            flag_change = True
        if flag_change:
            num_change += 1

        new_json = json.dumps(json_dict, indent=4, ensure_ascii=False)
        
        new_json_value = "```json\n" + new_json + "\n```"
        df.at[idx, 'json'] = new_json_value
    except Exception as e:
        print(f"Error at row {idx}: {e}")
        print(row['json'])
        continue

df.to_csv('data/time_reasoning/function_calling_v3.csv', index=False)

print(f"Num change: {num_change}")
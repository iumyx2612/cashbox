import pandas as pd
from llama_index.core.output_parsers.utils import extract_json_str as filter_json_markdown
import json


SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information

Tool schema:
{'type': 'function', 'function': {'name': 'calculate_time', 'description': 'calculate_time(today: Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\'], mentioned_date: Optional[Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\']] = None, week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today'], 'type': 'object'}}}
"""


path = 'data/data_time_cover/fc_time_data_250408_full.csv'

df = pd.read_csv(path)
print(len(df))
# apply new system prompt to system prompt column
df['system'] = SYSTEM_PROMPT

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
change_week = 0
new_df = pd.DataFrame(columns=df.columns)
for idx, row in df.iterrows():
    try:
        json_value = row['json']
        
        # answer = json.loads(row['answer'].replace("'", '"').replace("None", "null"))

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
        
        json_dict['today'] = today
        json_dict['mentioned_date'] = mentioned_date
        
        flag_change = False
        if mentioned_date is None: 
            new_df = new_df._append(row, ignore_index=True)
            continue
        else: 
            mentioned_array = DAY_ARRAY.index(mentioned_date)
            today_array = DAY_ARRAY.index(today)
            if mentioned_array > today_array and json_dict['week'] == 0: 
                json_dict['week'] = 1
                flag_change = True
                change_week += 1
        
        relation_date = json_dict['relative_date']
        if relation_date is not None and isinstance(relation_date, int): 
            json_dict['mentioned_date'] = None
            json_dict['week'] = 0
            flag_change = True
            num_change += 1
        
        abs_date = json_dict['absolute_date']
        if abs_date is not None and isinstance(abs_date, str): 
            json_dict['mentioned_date'] = None
            json_dict['relative_date'] = None
            json_dict['week'] = 0
            flag_change = True
            num_change += 1
        # if flag_change:
        #     num_change += 1

        new_json = json.dumps(json_dict, indent=4, ensure_ascii=False)
        
        new_json_value = "```json\n" + new_json + "\n```"
        row['json'] = new_json_value
        new_df = new_df._append(row, ignore_index=True)
    except Exception as e:
        print(f"-----------------------\nError at row {idx}: {e}")
        print(row['json'])
        print(row['answer'])
        print("------------------------")
        continue

new_df.to_csv('data/data_time_cover/time_fix_v1.csv', index=False, encoding='utf-8')
print(len(new_df))
print(f"Num change: {num_change}")
print(f"Num change week: {change_week}")
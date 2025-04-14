import pandas as pd

SYSTEM = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information

Tool schema:
{'type': 'function', 'function': {'name': 'calculate_time', 'description': 'calculate_time(today: Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], mentioned_date: Optional[Literal['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật']] = None, week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today'], 'type': 'object'}}}
"""


# path1 = 'data/time_reasoning/function_calling/last_merged_time_absolute.csv'
# path2 = 'data/data_time_cover_v3/function_calling_v6_done.csv' 
path1 = 'data/data_time_cover_v3/function_calling_v7-done.csv'
path2 = 'data/data_time_cover_v3/fc_time_data_250410_full.csv'

df1 = pd.read_csv(path1)
df1 = df1[['system', 'user', 'json']]
print(f"df1 shape: {len(df1)}")
df2 = pd.read_csv(path2)
df2 = df2[['system', 'user', 'json']]
print(f"df2 shape: {len(df2)}") 

df3 = pd.concat([df1, df2], ignore_index=True)
print(f"df3 shape: {len(df3)}")
# only get 3 columns : system, user, new_json

# df3 = df3[['system', 'user', 'new_json']]
# # change new_json to json
# df3.rename(columns={'new_json': 'json'}, inplace=True)

df3 = df3.drop_duplicates(subset=['user'], keep='first')
# keep the first duplicate and remove the rest
print(len(df3))
df3['system'] = SYSTEM
df3.to_csv('data/data_time_cover_v3/function_calling_v8.csv', index=False, encoding='utf-8')

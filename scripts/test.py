import pandas as pd
import ast
import json
df = pd.read_csv('format_data/money_v1.csv')

df = df['text'].tolist()
# print(df[:1])

new_df = []
for i in df: 
    try: 
        row = ast.literal_eval(i)
        value = int(float(str(row[-1]['content'])))
        _row = [row[0]['content'], row[1]['content'], value] 
        new_df = new_df + [_row]
        # row[-1]['content'] = f'{(int(float(str(row[-1]['content']))))}'
        # _row = json.dumps(row)
        # # print(_row)
        # new_df.append((_row))  # Convert row to string before appending
    except: 
        print(i)
     
# save to csv with columns = ['system', 'user', 'json']
new_df = pd.DataFrame(new_df, columns=['system', 'user', 'json'])
new_df.to_csv('format_data/money_v1_formatted.csv', index=False, encoding="utf-8")
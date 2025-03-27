import pandas as pd 


list_file = [
'data_baseline_v4/baseline_v3.csv', 
'data_baseline_v4/5xxx_concai.csv', 
'data_baseline_v4/cover_data_250322.csv', 
]


df = pd.DataFrame(columns=['system', 'user', 'json'])

for file in list_file:
    print(file)
    df_tmp = pd.read_csv(file)
    # just get 3 columns: system, user, json
    df_tmp = df_tmp[['system', 'user', 'json']]
    # remove header 
    df_tmp = df_tmp.iloc[1:]
    # remove empty lines
    df_tmp = df_tmp.dropna()
    # remove duplicate lines
    df_tmp = df_tmp.drop_duplicates()
    # concat df_tmp to df
    df = pd.concat([df, df_tmp], ignore_index=True)

df.to_csv('data_baseline_v4/baseline_v4.csv', index=False, encoding='utf-8')
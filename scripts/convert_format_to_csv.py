import pandas as pd 


list_file = [
    'money_data_v2/money_v2.csv', 
    'money_data_v2/bil_data.csv', 
    'money_data_v2/mil_new.csv', 
]


df = pd.DataFrame(columns=['system', 'user', 'json'])

for file in list_file:
    df_tmp = pd.read_csv(file) 
    # remove header 
    df_tmp = df_tmp.iloc[1:]
    # remove empty lines
    df_tmp = df_tmp.dropna()
    # remove duplicate lines
    df_tmp = df_tmp.drop_duplicates()
    # concat df_tmp to df
    df = pd.concat([df, df_tmp], ignore_index=True)

df.to_csv('money_data_v2/money_v3.csv', index=False)
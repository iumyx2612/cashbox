import pandas as pd 
import os

list_file = [
    'data/data_category/merge_category_data.csv', 
    'data/data_baseline_v8/baseline_v8.csv',
]

# list_file = []
# for filename in os.listdir('data/data_category/results'):
#     list_file.append(os.path.join('data/data_category/results', filename))
print("list file:", list_file)

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
    print(len(df_tmp))
    print(df_tmp.info())
    # concat df_tmp to df
    df = pd.concat([df, df_tmp], ignore_index=True)

print("data after add :", len(df))
# remove duplicate lines
df = df.drop_duplicates()
print("data after remove duplicate:", len(df))
# remove empty lines
df = df.dropna()
print("data after remove empty lines:", len(df))

df.to_csv('data/data_baseline_v8/baseline_v8_category.csv', index=False, encoding='utf-8')

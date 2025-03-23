import pandas as pd 

df = pd.read_csv('data_baseline_v4/value_data_v3.csv')
print(df.head())
print(df.info())

# remove \n from system columns, which appear at the first character
# df['system'] = df['system'].str.lstrip('\n')
# # remove " from user columns 
# df['user'] = df['user'].str.replace('"', '')
# # remove \n from user columns
# df['user'] = df['user'].str.replace('\n', ' ')
# df['json'] = df['json'].str.replace('\n', '')

# df.to_csv('data_baseline_v4/value_data_v3.csv', index=False, encoding='utf-8')
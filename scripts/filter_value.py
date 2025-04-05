import pandas as pd
import os
folder_save = 'data_baseline_v7/trieu'

if not os.path.exists(folder_save):
    os.makedirs(folder_save)
 
VALUE_KEYWORDS = [
    ' mê', ' chai', ' trai', ' củ ', ' triệu'
]

df = pd.read_csv('data_baseline_v7/baseline_v7_clean_time_abs.csv')
print(len(df)) 


for value in VALUE_KEYWORDS:
    # check if column json contains the value then get this row 
    df_filter = df[df['user'].str.contains(value, na=False)]
    # remove duplicates, and na values
    df_filter = df_filter.drop_duplicates()
    df_filter = df_filter.dropna()
    # remove rows with empty strings
    df_filter = df_filter[df_filter['json'] != '']
    # save to csv file
    print(f'len {value}: {len(df_filter)}')
    df_filter.to_csv(f'{folder_save}/baseline_v7_clean_time_{value}.csv', index=False, encoding='utf-8')

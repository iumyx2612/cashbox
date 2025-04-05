import pandas as pd 
import os

path = 'data/time_reasoning/function_calling'

new_df = pd.DataFrame(columns=['system', 'user', 'json', 'answer'])
for file in os.listdir(path): 
    print(file)
    if file.endswith('.csv'):
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        # remove headers
        df = df.iloc[1:]
        print(len(df)) 
        new_df = pd.concat([new_df, df], ignore_index=True)

new_df.to_csv('data/time_reasoning/function_calling.csv', index=False, encoding='utf-8')
print(len(new_df))


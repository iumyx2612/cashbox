import pandas as pd
import os


for file_name in os.listdir('data_time_reasoning'):
    if file_name.endswith('.csv'):
        file_path = os.path.join('data_time_reasoning', file_name)
        df = pd.read_csv(file_path)
        
        # filter row where texts in column 'text' contains 'Dưới đây là' hoặc 'Sure! Here are 10 sentences' 
        # then remove this row
        df = df[~df['user'].str.contains('Dưới đây là|Here are 10 sentences|Here are', na=False)]
        # then save this dataframe to a new csv file
        new_file_name = file_name.replace('.csv', '_filtered.csv')
        new_file_path = os.path.join('data_time_reasoning', new_file_name)
        df.to_csv(new_file_path, index=False, encoding='utf-8')
        print(f"Filtered data saved to {new_file_path}")
         
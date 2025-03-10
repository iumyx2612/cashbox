# import pandas as pd
# import os
# import sys
# from pathlib import Path    
# sys.path.append(str(Path(__file__).resolve().parents[1]))


# file_name = ['mil_formatted.csv', 'money_v1_formatted_autotrain.csv'] 


# # concat all files into one file
# new_df = pd.DataFrame(columns=['text'])
# for file in file_name: 
#     file_path = '/home/hoang.minh.an/anhalu-data/learning/cashbox/format_data/' + file
#     df = pd.read_csv(file_path)
#     new_df = pd.concat([new_df, df], ignore_index=True)
    
# new_df.to_csv('/home/hoang.minh.an/anhalu-data/learning/cashbox/format_data/money_v2_formatted_value.csv', index=False)


import pandas as pd 

df = pd.read_csv("data/mil (2).csv")   
df.to_excel('data/mil.xlsx', index=False)

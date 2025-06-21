import pandas as pd 


path = 'data/time_reasoning/function_calling_v3.csv'
df = pd.read_csv(path)


print(df.iloc[1000]['system'])
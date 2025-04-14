import pandas as pd

path = 'data/data_baseline_v9/baseline_v9_category_fix_time.csv' 
df = pd.read_csv(path)
print(f"len(df)", len(df))

path2 = 'data/data_time_cover_v3/function_calling_v8.csv' 
df2 = pd.read_csv(path2)
print(f"len(df2)", len(df2))

path3 = 'data/data_category_v2/merged_results.csv'
df3 = pd.read_csv(path3)
print(f"len(df3)", len(df3))

merge = pd.concat([df, df2, df3], ignore_index=True)
print(len(merge)) 
merge = merge.drop_duplicates(subset=['user'], keep='first')
merge = merge.dropna(subset=['json'])
print(len(merge)) 
merge.to_csv('data/data_baseline_v9/baseline_time_function_calling_v1.csv', index=False, encoding='utf-8')

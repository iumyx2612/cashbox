import pandas as pd 

path = 'data/data_baseline_v8/baseline_v8_category.csv'
# path = 'data/time_reasoning/data_time_reasoning.csv'
df = pd.read_csv(path)

row = df.iloc[0]
num_rangdom_rows = 10
new_df = pd.DataFrame(columns=df.columns)
# print(row['json'])
for i in range(20):
    filter_value = f'"relative_date": -{i}' if i > 0 else '"relative_date": 0'
    filtered_df = df[df['json'].str.contains(filter_value, na=False)]
    # print(f'filtered_df for {i} : {len(filtered_df)}:')
    # get random num rangdom rows from filtered_df
    if len(filtered_df) >= num_rangdom_rows:
        filtered_df_random = filtered_df.sample(n=num_rangdom_rows, random_state=2)
    else:
        filtered_df_random = filtered_df.sample(n=len(filtered_df), random_state=2)
    print(f'filtered_df_random for {len(filtered_df_random)}:')

    new_df = pd.concat([new_df, filtered_df_random], ignore_index=True)

print(len(new_df))
new_df.to_csv('data/data_baseline_v8/baseline_v8_category_random.csv', index=False)
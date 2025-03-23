import pandas as pd 
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import os


GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

# client = OpenAI(
#     base_url="http://10.0.7.50:8011/v1",
#     api_key="emansieuvc"
# )


df = pd.read_excel('data_test/data_test.xlsx')
acc = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try: 
        # Task all
        sentence = row['Example']
        user_prompt = f"{sentence.rstrip('\n')}"
        
        completion = client.chat.completions.create(
            model="/qwen-baseline-money-v5",
            messages=[
                {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        
        # print(completion.choices[0].message.content)    
        output = completion.choices[0].message.content
        int_output = int(float(str(output)))
        true_value = int(float(str(row['Giá trị'])))
        if int_output != true_value:
            print(f"input : {sentence}")
            print("label: ", true_value)
            print("output model: ", int_output)
            print("====================")
        
        if int_output == true_value:
            acc.append(1)
        else:
            acc.append(0)
        df.at[index, 'output'] = int_output
 
    except Exception as e:
        print(e)

df.to_excel('data_test/data_test_output_v2.xlsx', index=False, engine='xlsxwriter')  

if len(acc) > 0:
    print("Mean: ", sum(acc)/len(acc))
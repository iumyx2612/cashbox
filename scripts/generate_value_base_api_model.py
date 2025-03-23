from openai import OpenAI
import re
import json
import pandas as pd
from tqdm import tqdm
import os
from openai import OpenAI


GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
"""

GEN_VALUE_SYSTEM_WITHOUT_EXM_V2 = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
EXAMPLE:
Mới thanh toán tiền học cho con củ chín.
Output:
1900000
"""
example = "Ra cửa hàng thời trang mua đôi giày mất mờ 5."
example_output = "1500000"
client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="dmeman"
)

# client = OpenAI(
#     api_key=os.getenv("openai_key"),
# )

with open('/home/hoang.minh.an/anhalu-data/learning/cashbox/data/all/value_special.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]  # remove empty lines
    

df = pd.DataFrame(columns=['system', 'user', 'json'])
for line in tqdm(lines): 
    
    try: 
        # Task all
        sentence = line
        user_prompt = f"""{sentence}"""
        print(f"input : {sentence}")
        completion = client.chat.completions.create(
            model="models/qwen-baseline-money-v2",
            # model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM_V2},
                {"role": "user", "content": example}, 
                {"role": "assistant", "content": example_output},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )

        # print(completion.choices[0].message.content)    
        output = completion.choices[0].message.content

        value = int(float(str(output)))
        print(value)
        # Append the result to the DataFrame
        df = df._append({
            'system': GEN_VALUE_SYSTEM_WITHOUT_EXM,
            'user': user_prompt,
            'json': value
        }, ignore_index=True)
    except Exception as e: 
        print(e)

# Save the DataFrame to an Excel file
df.to_excel('value_special_em_An.xlsx', index=False)
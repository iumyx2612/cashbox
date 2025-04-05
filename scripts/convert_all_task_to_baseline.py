import pandas as pd
import json
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
from openai import OpenAI
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, GEN_FORMAT_USER_STR, DAY_MAPPING, EXAMPLE
from cores.utils import filter_json_markdown
from tqdm import tqdm
import re 

GEN_JSON_SAVE = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user

Here's a JSON schema to follow:
{{""$defs"": {{""CashCategory"": {{""description"": ""Only exist ONE field. Field value CAN be null"", ""properties"": {{""food"": {{""anyOf"": [{{""enum"": [""Đồ uống"", ""Ăn sáng"", ""Ăn trưa"", ""Ăn tối"", ""Ăn vặt""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used for food"", ""title"": ""Food""}}, ""commute"": {{""anyOf"": [{{""enum"": [""Xăng xe"", ""Gửi xe"", ""Bảo hiểm xe"", ""Thuê xe"", ""Sửa chữa xe""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to commute"", ""title"": ""Commute""}}, ""health_care"": {{""anyOf"": [{{""enum"": [""Khám chữa bệnh"", ""Thuốc men"", ""Thể thao"", ""Bảo hiểm y tế""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to health care"", ""title"": ""Health Care""}}, ""living_expense"": {{""anyOf"": [{{""enum"": [""Tiền điện"", ""Tiền nước"", ""Tiền internet"", ""Tiền gas"", ""Tiền truyền hình"", ""Tiền điện thoại"", ""Tiền siêu thị""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to living expenses"", ""title"": ""Living Expense""}}, ""child_care"": {{""anyOf"": [{{""enum"": [""Học phí"", ""Trông trẻ"", ""Tiền sữa"", ""Tiền bỉm"", ""Tiền đồ chơi"", ""Tiền tiêu vặt""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to child care"", ""title"": ""Child Care""}}, ""clothing"": {{""anyOf"": [{{""enum"": [""Quần áo"", ""Giầy dép"", ""Phụ kiện khác""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to clothing or body accessories"", ""title"": ""Clothing""}}, ""household"": {{""anyOf"": [{{""enum"": [""Đồ đạc trong nhà"", ""Tiền thuê nhà"", ""Thế chấp nhà"", ""Sửa nhà""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to household"", ""title"": ""Household""}}, ""treat_money"": {{""anyOf"": [{{""enum"": [""Vui chơi giải trí"", ""Du lịch"", ""Phim ảnh ca nhạc"", ""Spa & Massage"", ""Mỹ phẩm""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used to enjoy or reward yourself"", ""title"": ""Treat Money""}}, ""self_growth"": {{""anyOf"": [{{""enum"": [""Học hành"", ""Xây dựng mối quan hệ""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money invest in yourself for self improvement"", ""title"": ""Self Growth""}}, ""bank"": {{""anyOf"": [{{""enum"": [""Phí chuyển khoản"", ""Trả lãi vay"", ""Trả nợ ngân hàng""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to bank"", ""title"": ""Bank""}}, ""invest"": {{""anyOf"": [{{""enum"": [""Chứng khoán"", ""Vàng"", ""Tiền số"", ""Trái phiếu"", ""Nhà đất""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used in investment"", ""title"": ""Invest""}}}}, ""title"": ""CashCategory"", ""type"": ""object""}}, ""TimeInformation"": {{""properties"": {{""absolute_date"": {{""anyOf"": [{{""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Date in dd-mm format. Null if specific date is not mentioned"", ""title"": ""Absolute Date""}}, ""relative_date"": {{""default"": 0, ""description"": ""How many days from today to said day. Use default value if not mentioned"", ""maximum"": 0, ""title"": ""Relative Date"", ""type"": ""integer""}}}}, ""title"": ""TimeInformation"", ""type"": ""object""}}}}, ""properties"": {{""spent_or_received"": {{""description"": ""Is the money spent on things or received from another. True for spent, False for received"", ""title"": ""Spent Or Received"", ""type"": ""boolean""}}, ""category"": {{""$ref"": ""#/$defs/CashCategory""}}, ""when"": {{""$ref"": ""#/$defs/TimeInformation""}}, ""object"": {{""description"": ""The object that affects the money mentioned in the sentence."", ""title"": ""Object"", ""type"": ""string""}}, ""who"": {{""anyOf"": [{{""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""The person mentioned in the sentence"", ""title"": ""Who""}}, ""value"": {{""description"": ""Amount of money"", ""title"": ""Value"", ""type"": ""integer""}}}}, ""required"": [""spent_or_received"", ""category"", ""when"", ""object"", ""value""], ""title"": ""CashFlowInformation"", ""type"": ""object""}}

Output a valid JSON object but do not repeat the schema.
"""


GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

model_name = '/qwen-baseline-money-v5'

df = pd.read_csv('data_baseline_v4/baseline_v4.csv')
# print(len(df))


def predict_value(sentence: str) -> int: 
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM},
            {"role": "user", "content": sentence}
        ], 
        temperature=0
    )

    return response.choices[0].message.content


def predict_task_all(sentence: str): 
    day = "Thứ hai"
    user_prompt = GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": GEN_FORMAT_SYSTEM_STR.format(example=EXAMPLE)},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )

    return filter_json_markdown(response.choices[0].message.content), user_prompt

baseline_df = pd.DataFrame(columns=['system', 'user', 'json'])
for idx, row in tqdm(df.iterrows()):
    try: 
        system_prompt = GEN_JSON_SAVE
        user_prompt = str(row['user']).rstrip('\n')
        user_prompt_str = re.sub(r'Note that today is.*', '', user_prompt)
        assistant_prompt = row['json']
        
        
        if 'Note that today is' in user_prompt:    
            # get dict from assistant_prompt
            assistant_str = filter_json_markdown(assistant_prompt)
            try: 
                assistant_dict = json.loads(assistant_str)
            except json.JSONDecodeError:
                # print(f"Error decoding JSON at index {idx}: {assistant_prompt}, assistant_str: {assistant_str}")
                continue
            
            if 'spent_or_received' in assistant_dict: 
                # predict value from user prompt str ``
                value = predict_value(user_prompt_str)
                
                # add value to assistant_dict
                assistant_dict['value'] = str(value)
                
                json_str = json.dumps(assistant_dict, indent=4, ensure_ascii=False)
                
                # add system prompt, user prompt, assistant prompt to baseline_df
                baseline_df = baseline_df._append({
                    "system": system_prompt,
                    "user": user_prompt,
                    "json": f"""```json\n{json_str}\n```"""
                }, ignore_index=True)
                continue
        
        # all other cases : run predict_task_all first then predict_value.
        # predict task all
        new_assistant_prompt, user_prompt_with_note = predict_task_all(user_prompt)
        new_assistant_dict = json.loads(new_assistant_prompt)
        
        # check if can convert assistant prompt to int or not
        try: 
            value = int(new_assistant_dict['value'])
        except ValueError:
            # predict value from user prompt str
            value = predict_value(user_prompt_str)
        
        # then add value to new assistant_dict 
        new_assistant_dict['value'] = str(value)
        # then convert to json string
        json_str = json.dumps(new_assistant_dict, indent=4, ensure_ascii=False)
        # add system prompt, user prompt, assistant prompt to baseline_df
        baseline_df = baseline_df._append({
            "system": system_prompt,
            "user": user_prompt_with_note,
            "json": f"""```json\n{json_str}\n```"""
        }, ignore_index=True)
    except Exception as e:
        print(idx)
        # print(f"Error at index {idx}: {e}")
        # print(f"User prompt: {user_prompt}")
        # print(f"Assistant prompt: {assistant_prompt}")
        continue
    
# save baseline_df to csv
baseline_df.to_csv('data_baseline_v4/baseline_v4.csv', index=False, encoding='utf-8')

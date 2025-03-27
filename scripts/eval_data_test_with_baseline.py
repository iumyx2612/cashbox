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

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

# client = OpenAI(
#     base_url="http://10.0.7.50:8011/v1",
#     api_key="emansieuvc"
# )
model_name = '/qwen-baseline-money-v6-1'

def predict_task_all(sentence: str): 
    day = "Thứ hai"
    user_prompt = GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": GEN_JSON_SAVE},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )

    return filter_json_markdown(response.choices[0].message.content)


df = pd.read_excel('data_test/data_test.xlsx')

acc = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try: 
        # Task all
        sentence = row['Example']
        baseline_task_str = predict_task_all(sentence)
        baseline_task_dict = json.loads(baseline_task_str)
        
        int_output = int(float(baseline_task_dict['value']))
        
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

df.to_excel('data_test/data_test_output_model-v6-1.xlsx', index=False, engine='xlsxwriter')  

if len(acc) > 0:
    print("Mean: ", sum(acc)/len(acc))
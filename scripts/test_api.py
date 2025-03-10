from openai import OpenAI
import re
import json
import pandas as pd
from tqdm import tqdm
all_task = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence

Here's a JSON schema to follow:
{{"$defs": {{"CashCategory": {{"description": "Only exist ONE field. Field value CAN be null", "properties": {{"food": {{"anyOf": [{{"enum": ["Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for food", "title": "Food"}}, "commute": {{"anyOf": [{{"enum": ["Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xê", "Sửa chữa xe"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to commute", "title": "Commute"}}, "health_care": {{"anyOf": [{{"enum": ["Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to health care", "title": "Health Care"}}, "living_expense": {{"anyOf": [{{"enum": ["Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas", "Tiền truyền hình", "Tiền điện thoại", "Tiền siêu thị"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to living expenses", "title": "Living Expense"}}, "child_care": {{"anyOf": [{{"enum": ["Học phí", "Trông trẻ", "Tiền sữa", "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to child care", "title": "Child Care"}}, "clothing": {{"anyOf": [{{"enum": ["Quần áo", "Giầy dép", "Phụ kiện khác"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to clothing or body accessories", "title": "Clothing"}}, "household": {{"anyOf": [{{"enum": ["Đồ đạc trong nhà", "Tiền thuê nhà", "Thế chấp nhà", "Sửa nhà"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to household", "title": "Household"}}, "treat_money": {{"anyOf": [{{"enum": ["Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc", "Spa & Massage", "Mỹ phẩm"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used to enjoy or reward yourself", "title": "Treat Money"}}, "self_growth": {{"anyOf": [{{"enum": ["Học hành", "Xây dựng mối quan hệ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in yourself for self improvement", "title": "Self Growth"}}, "bank": {{"anyOf": [{{"enum": ["Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to bank", "title": "Bank"}}, "invest": {{"anyOf": [{{"enum": ["Chứng khoán", "Vàng", "Tiền số", "Trái phiếu", "Nhà đất"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used in investment", "title": "Invest"}}}}, "title": "CashCategory", "type": "object"}}, "TimeInformation": {{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to said day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}}}, "properties": {{"spent_or_received": {{"description": "Is the money spent on things or received from another. True for spent, False for received", "title": "Spent Or Received", "type": "boolean"}}, "category": {{"$ref": "#/$defs/CashCategory"}}, "when": {{"$ref": "#/$defs/TimeInformation"}}, "object": {{"description": "The object that affects the money mentioned in the sentence.", "title": "Object", "type": "string"}}, "who": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "The person mentioned in the sentence", "title": "Who"}}, "value": {{"description": "Amount of money", "title": "Value", "type": "integer"}}}}, "required": ["spent_or_received", "category", "when", "object", "value"], "title": "CashFlowInformation", "type": "object"}}
Output a valid JSON object but do not repeat the schema."""



Only_value = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""


client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="dmeman"
)

data_df = pd.read_excel('data/Data Test (1).xlsx') 
print(data_df.head())

value = data_df['Giá trị'].tolist()
example = data_df['Example'].tolist()

predict_column_task_all = []
acc_task_all = []


predict_column_task_value = []
acc_task_value = []
for va, ex in tqdm(zip(value, example)):
  try: 
    # Task all
    va = int(float(str(va)))
    sentence = ex
    day = "Thứ 5"
    user_prompt = f"""{sentence}\nNote that today is {day}"""
    print(f"input : {sentence}")
    completion = client.chat.completions.create(
      model="models/qwen-baseline-money-v2",
      messages=[
        {"role": "system", "content": all_task},
        {"role": "user", "content": user_prompt}
      ],
      temperature=0
    )

    # print(completion.choices[0].message.content)    
    output = completion.choices[0].message.content

    match = re.search(r'```json\n(.*?)\n```', output, re.DOTALL)
    if match:
        json_str = match.group(1)  # Lấy nội dung JSON
        data = json.loads(json_str)  # Chuyển thành dictionary
    else:
        print(f"Không tìm thấy JSON task all, {output}")
        data = None
    print("task all : ", data)
    value_all = int(float(str(data['value']))) if data else 'error'

  except: 
    value_all = 'error'
  predict_column_task_all.append(value_all)
  
  if value_all != 'error' and va == value_all:
    acc_task_all.append(1)
  else:
    acc_task_all.append(0)

  # do the same for task value, let's use Only_value and sentence is user_prompt
  try: 
    va = int(float(str(va)))
    sentence = ex
    # not need day 
    user_prompt = f"""{sentence}"""
    completion = client.chat.completions.create(
      model="models/qwen-baseline-money-v2",
      messages=[
        {"role": "system", "content": Only_value},
        {"role": "user", "content": user_prompt}
      ],
      temperature=0
    )
    
    # print(completion.choices[0].message.content)
    output = completion.choices[0].message.content
    print("task value : ", output)
    value = int(float(str(output)))
      
    predict_column_task_value.append(value)
  except:
    value = 'error'
    predict_column_task_value.append(value) 
  if value != 'error' and va == value:
    acc_task_value.append(1)
  else:
    acc_task_value.append(0)

print("Accuracy: ", sum(acc_task_all)/len(acc_task_all))
print("Accuracy: ", sum(acc_task_value)/len(acc_task_value))


# add new column to data_df
data_df['Predict task all'] = predict_column_task_all
data_df['Predict task value'] = predict_column_task_value

# save data_df to excel
data_df.to_excel('data/data_test_predict.xlsx', index=False)
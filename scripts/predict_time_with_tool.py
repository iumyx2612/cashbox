import json
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
import time
from openai import OpenAI
from cores.schema.time_tool import calculate_time
from cores.prompts.gen_json import GEN_FORMAT_USER_STR
from cores.utils import filter_json_markdown

TIME_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information
Note you must use the tool to calculate the time difference between mentioned date and today.

Tool schema:
{'name': 'calculate_time', 'description': 'calculate_time(today: Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\'], mentioned_date: Optional[Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\']] = None, week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today'], 'type': 'object'}}}
"""

BASELINE_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user

Here's a JSON schema to follow:
{{"$defs": {{"CashCategory": {{"description": "Only exist ONE field. Field value CAN be null", "properties": {{"food": {{"anyOf": [{{"enum": ["Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for food", "title": "Food"}}, "commute": {{"anyOf": [{{"enum": ["Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xe", "Sửa chữa xe", "Thuế phí"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to commute", "title": "Commute"}}, "health_care": {{"anyOf": [{{"enum": ["Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to health care", "title": "Health Care"}}, "living_expense": {{"anyOf": [{{"enum": ["Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas", "Tiền truyền hình", "Tiền điện thoại"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to living expenses", "title": "Living Expense"}}, "shopping": {{"anyOf": [{{"enum": ["Tiền siêu thị", "Tiền đi chợ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to shopping", "title": "Shopping"}}, "child_care": {{"anyOf": [{{"enum": ["Học phí", "Trông trẻ", "Tiền sữa", "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to child care", "title": "Child Care"}}, "clothing": {{"anyOf": [{{"enum": ["Quần áo", "Giầy dép", "Phụ kiện khác"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to clothing or body accessories", "title": "Clothing"}}, "gifts_donations": {{"anyOf": [{{"enum": ["Thăm hỏi", "Biếu tặng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for gifts or donations", "title": "Gifts Donations"}}, "household": {{"anyOf": [{{"enum": ["Đồ đạc trong nhà", "Tiền thuê nhà", "Sửa nhà"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to household", "title": "Household"}}, "treat_money": {{"anyOf": [{{"enum": ["Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc", "Spa & Massage", "Mỹ phẩm", "Nhậu nhẹt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used to enjoy or reward yourself", "title": "Treat Money"}}, "pets": {{"anyOf": [{{"enum": ["Chó", "Mèo"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in your pets", "title": "Pets"}}, "self_growth": {{"anyOf": [{{"enum": ["Học hành", "Xây dựng mối quan hệ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in yourself for self improvement", "title": "Self Growth"}}, "bank": {{"anyOf": [{{"enum": ["Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to bank", "title": "Bank"}}, "invest": {{"anyOf": [{{"enum": ["Chứng khoán", "Vàng", "Tiền số", "Nhà đất"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used in investment", "title": "Invest"}}, "saving": {{"anyOf": [{{"enum": ["Gửi tiền tiết kiệm", "Cho vay"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for saving or lending", "title": "Saving"}}, "income": {{"anyOf": [{{"enum": ["Lương", "Thưởng", "Thu hồi nợ", "Kinh doanh", "Trợ cấp", "Rút tiết kiệm", "Bán tài sản"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for income", "title": "Income"}}}}, "title": "CashCategory", "type": "object"}}, "TimeInformation": {{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to said day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}}}, "properties": {{"spent_or_received": {{"description": "Is the money spent on things or received from another. True for spent, False for received", "title": "Spent Or Received", "type": "boolean"}}, "category": {{"$ref": "#/$defs/CashCategory"}}, "when": {{"$ref": "#/$defs/TimeInformation"}}, "object": {{"description": "The object that affects the money mentioned in the sentence.", "title": "Object", "type": "string"}}, "who": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "The person mentioned in the sentence", "title": "Who"}}, "value": {{"description": "Amount of money", "title": "Value", "type": "integer"}}}}, "required": ["spent_or_received", "category", "when", "object", "value"], "title": "CashFlowInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
"""

# baseline 
client = OpenAI(
    base_url="http://10.0.4.239:8011/v1",
    api_key="emansieuvc"
)
model_name_baseline = '/qwen-baseline-money-v8-category'

def predict_baseline(user_prompt: str):
    completion = client.chat.completions.create(
    model=model_name_baseline,
    messages=[
        {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0
    )
    return filter_json_markdown(completion.choices[0].message.content)

# time
llm = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc", 
)
model_name = '/qwen-time-function-calling-v2'

def predict_time(user_prompt: str): 
    response = llm.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": TIME_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0,
    )
    
    time_str = response.choices[0].message.content
    time_dict = json.loads(filter_json_markdown(time_str)) 
    time_value_from_tool = calculate_time(**time_dict)
    return time_value_from_tool, time_str


# sentence = "Sáng hôm qua đã đi vào đà nẵng hết 6 củ"
# sentence = "Hôm kia đóng tiền điện hết 1 củ ba"
sentence = "Thứ năm hai tuần trước đi cafe với hội đồng hương Phú Thọ 8 sịch"
# sentence = "chiều qua mua hai chục hoa hồng 80 cành"
day = 'Chủ Nhật'
start = time.time() 
user_prompt = GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)
print("User prompt: \n", user_prompt)
baseline = predict_baseline(user_prompt)
end_baseline = time.time()
print("baseline : \n", baseline)
start_time = time.time()
time_vlue_from_tool, time_str = predict_time(user_prompt)
end_time = time.time()
print("\n\nTime tool : \n", time_str)
print("time_vlue_from_tool : \n", time_vlue_from_tool)
print("\n\nTime taken for baseline: ", end_baseline - start)
print("Time taken for time: ", end_time - start_time)
print("Time taken for total: ", end_time - start)
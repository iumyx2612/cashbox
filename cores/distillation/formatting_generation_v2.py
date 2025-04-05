import json
import pandas as  pd 
import json
from tqdm import tqdm
from cores.utils import filter_example_block
from cores.schema.category import CashCategory
from cores.schema.time import TimeInformation
from cores.schema.cashbox import CashFlowInformation
from cores.prompts.gen_time import GEN_TIME_SYSTEM, GEN_TIME_USER, EXAMPLE
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, GEN_FORMAT_USER_STR, DAY_MAPPING
from cores.output_parser.vi_pydantic import ViPydanticOutputParser
from cores.utils import filter_json_markdown_anywhere, filter_json_markdown
import re
from openai import OpenAI

SYSTEM_MSG = """You are a money manager assistant.
Your job is to extract time information in JSON from provided sentence.

Here's a JSON schema to follow:
{{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to mentioned day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
Remember to think step by step
"""

client = OpenAI(
    base_url="http://10.0.7.50:8011/v1",
    api_key="emansieuvc", 
    timeout=20,
)

model_name = '/qwen-reasoning-time-v3'

def predict_time(user_prompt): 
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )
    raw_context = response.choices[0].message.content
    context = filter_json_markdown_anywhere(raw_context)
    context = context.replace('{{', '{').replace('}}', '}')
    
    # remove double "" in context
    context = re.sub(r'\"\"', '"', context)

    return context, raw_context

BASELINE_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user

Here's a JSON schema to follow:
{{"$defs": {{"CashCategory": {{"description": "Only exist ONE field. Field value CAN be null", "properties": {{"food": {{"anyOf": [{{"enum": ["Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for food", "title": "Food"}}, "commute": {{"anyOf": [{{"enum": ["Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xe", "Sửa chữa xe", "Thuế phí"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to commute", "title": "Commute"}}, "health_care": {{"anyOf": [{{"enum": ["Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to health care", "title": "Health Care"}}, "living_expense": {{"anyOf": [{{"enum": ["Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas", "Tiền truyền hình", "Tiền điện thoại"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to living expenses", "title": "Living Expense"}}, "shopping": {{"anyOf": [{{"enum": ["Tiền siêu thị", "Tiền đi chợ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to shopping", "title": "Shopping"}}, "child_care": {{"anyOf": [{{"enum": ["Học phí", "Trông trẻ", "Tiền sữa", "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to child care", "title": "Child Care"}}, "clothing": {{"anyOf": [{{"enum": ["Quần áo", "Giầy dép", "Phụ kiện khác"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to clothing or body accessories", "title": "Clothing"}}, "gifts_donations": {{"anyOf": [{{"enum": ["Thăm hỏi", "Biếu tặng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for gifts or donations", "title": "Gifts Donations"}}, "household": {{"anyOf": [{{"enum": ["Đồ đạc trong nhà", "Tiền thuê nhà", "Sửa nhà"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to household", "title": "Household"}}, "treat_money": {{"anyOf": [{{"enum": ["Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc", "Spa & Massage", "Mỹ phẩm", "Nhậu nhẹt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used to enjoy or reward yourself", "title": "Treat Money"}}, "pets": {{"anyOf": [{{"enum": ["Chó", "Mèo"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in your pets", "title": "Pets"}}, "self_growth": {{"anyOf": [{{"enum": ["Học hành", "Xây dựng mối quan hệ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in yourself for self improvement", "title": "Self Growth"}}, "bank": {{"anyOf": [{{"enum": ["Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to bank", "title": "Bank"}}, "invest": {{"anyOf": [{{"enum": ["Chứng khoán", "Vàng", "Tiền số", "Nhà đất"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used in investment", "title": "Invest"}}, "saving": {{"anyOf": [{{"enum": ["Gửi tiền tiết kiệm", "Cho vay"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for saving or lending", "title": "Saving"}}, "income": {{"anyOf": [{{"enum": ["Lương", "Thưởng", "Thu hồi nợ", "Kinh doanh", "Trợ cấp", "Rút tiết kiệm", "Bán tài sản"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for income", "title": "Income"}}}}, "title": "CashCategory", "type": "object"}}, "TimeInformation": {{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to said day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}}}, "properties": {{"spent_or_received": {{"description": "Is the money spent on things or received from another. True for spent, False for received", "title": "Spent Or Received", "type": "boolean"}}, "category": {{"$ref": "#/$defs/CashCategory"}}, "when": {{"$ref": "#/$defs/TimeInformation"}}, "object": {{"description": "The object that affects the money mentioned in the sentence.", "title": "Object", "type": "string"}}, "who": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "The person mentioned in the sentence", "title": "Who"}}, "value": {{"description": "Amount of money", "title": "Value", "type": "integer"}}}}, "required": ["spent_or_received", "category", "when", "object", "value"], "title": "CashFlowInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
"""

client_task_all = OpenAI(
    base_url="http://10.0.4.239:8015/v1",
    api_key="emansieuvc"
)

# client = OpenAI(
#     base_url="http://10.0.7.50:8011/v1",
#     api_key="emansieuvc"
# )
model_name_task_all = '/qwen-baseline-money-v8-1'

def predict_task_all(user_prompt: str): 
    response = client_task_all.chat.completions.create(
        model=model_name_task_all,
        messages=[
            {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )

    return filter_json_markdown(response.choices[0].message.content)

def category_to_pydantic(
        category: str,
        subcategory: str
) -> CashCategory:
    if category == "Ăn uống":
        if subcategory == "Đồ uống":
            model = CashCategory(food="Đồ uống")
        elif subcategory == "Ăn trưa":
            model = CashCategory(food="Ăn trưa")
        elif subcategory == "Ăn tối":
            model = CashCategory(food="Ăn tối")
        else:
            raise ValueError
        # TODO: write more logic later
    elif category == "Đi lại":
        if subcategory == "Xăng xe":
            model = CashCategory(commute="Xăng xe")
        elif subcategory == "Gửi xe":
            model = CashCategory(commute="Gửi xe")
        elif subcategory == "Bảo hiểm xe":
            model = CashCategory(commute="Bảo hiểm xe")
        elif subcategory == "Taxi/Thuê xe":
            model = CashCategory(commute="Thuê xe")
        elif subcategory == "Sửa chữa xe":
            model = CashCategory(commute="Sửa chữa xe")
        else:
            raise ValueError
    elif category == "Sức khoẻ":
        if subcategory == "Khám chữa bệnh":
            model = CashCategory(health_care="Khám chữa bệnh")
        elif subcategory == "Bảo hiểm y tế":
            model = CashCategory(health_care="Bảo hiểm y tế")
        elif subcategory == "Thể thao":
            model = CashCategory(health_care="Thể thao")
        else:
            raise ValueError
        # TODO: write more logic later
    elif category == "Dịch vụ sinh hoạt": 
        if subcategory == 'Điện': 
            model = CashCategory(living_expense='Tiền điện')
        else: 
            raise  ValueError
        
    elif category == 'Con cái': 
        if subcategory == "Bỉm":
            model = CashCategory(child_care="Tiền bỉm")
        elif subcategory == "Đồ chơi":
            model = CashCategory(child_care="Tiền đồ chơi")
        elif subcategory == "Học phí":
            model = CashCategory(child_care="Học phí")
        elif subcategory == "Sữa": 
            model = CashCategory(child_care="Tiền sữa")
        elif subcategory == "Tiền tiêu vặt":
            model = CashCategory(child_care="Tiền tiêu vặt")
        elif subcategory == "Trông trẻ":
            model = CashCategory(child_care="Trông trẻ")
        else:
            raise ValueError
    elif category == "Trang phục": 
        if subcategory == "Quần áo":
            model = CashCategory(clothing="Quần áo")
        elif subcategory == "Giầy dép":
            model = CashCategory(clothing="Giầy dép")
        elif subcategory == "Phụ kiện khác":
            model = CashCategory(clothing="Phụ kiện khác")
    elif category == "Hiếu hỉ":
        if subcategory == "Biếu tặng":
            model = CashCategory(gifts_donations="Biếu tặng")
        elif subcategory == "Thăm hỏi":
            model = CashCategory(gifts_donations="Thăm hỏi")
        else:
            raise ValueError
    elif category == 'Nhà cửa':
        if subcategory == "Mua sắm đồ đạc":
            model = CashCategory(household="Đồ đạc trong nhà")
        elif subcategory == "Thuê nhà":
            model = CashCategory(household="Tiền thuê nhà")
        elif subcategory == "Sửa chữa":
            model = CashCategory(household="Sửa nhà")
        else:
            raise ValueError
    
    elif category == 'Hưởng thụ':  
        if subcategory == "Vui trơi giải trí":
            model = CashCategory(treat_money="Vui chơi giải trí")
        elif subcategory == "Du lịch":
            model = CashCategory(treat_money="Du lịch")
        elif subcategory == "Mỹ phẩm":
            model = CashCategory(treat_money="Mỹ phẩm")
        elif subcategory == "Nhậu nhẹt":
            model = CashCategory(treat_money="Nhậu nhẹt")
        elif subcategory == "Spa & massage":
            model = CashCategory(treat_money="Spa & Massage")
        elif subcategory == "Phim ảnh ca nhạc":
            model = CashCategory(treat_money="Phim ảnh ca nhạc")
        else:
            raise ValueError
    elif category == 'Thú cưng':
        if subcategory == "Chó":
            model = CashCategory(pets="Chó")
        elif subcategory == "Mèo":
            model = CashCategory(pets="Mèo")
        else:
            raise ValueError
    return model

def convert_zalo_v2(
        input_file: str,
        output_file: str,

) -> None:
    fp = open(input_file, 'r', encoding="utf-8")
    datas = json.load(fp)
    out_df = pd.DataFrame()

    for idx, data in tqdm(enumerate(datas), total=len(datas)):
        sentence = data.get("content", None) 
        type = data.get("type", None)
        category = data.get("category", None)
        subcategory = data.get("subcategory", None)
        object = data.get("object", None)
        who = data.get("who", None)
        
        if type == "chi":
            spent = True
        else:
            spent = False

        cash_category = category_to_pydantic(category, subcategory)
        cash_category = cash_category.model_dump(exclude_none=True)
        try: 
            value = int(float(str(data.get('money_value',  None))))
        except Exception as e:
            print(f"Error while converting value idx {idx} : {e}, value : {data.get('money_value',  None)}")
            continue
        day = "Thứ hai"
        user_str = GEN_TIME_USER.format(sentence=sentence, day=day)
        try: 
            basline_str = predict_task_all(user_str)
            baseline_dict = json.loads(basline_str)
            time_json = baseline_dict['when']
        except Exception as e:
            print(f"Error in time generation idx {idx} : {e}")
            continue

        json_dict = {
            "spent_or_received": spent,
            "category": cash_category,
            "when": time_json,
            "object": object,
            "who": who,
            "value": value
        }

        json_str = json.dumps(json_dict, indent=4, ensure_ascii=False)

        output_parser = ViPydanticOutputParser(CashFlowInformation)
        format_str = output_parser.format_string
        system_str = GEN_FORMAT_SYSTEM_STR.format(example=EXAMPLE)
        system_str = filter_example_block(system_str)
        system_str = f"{system_str}\n{format_str}"
        out_df = out_df._append({
            "system": system_str,
            "user": user_str,
            "json": f"""```json\n{json_str}\n```"""
        }, ignore_index=True)
          

    out_df.to_csv(output_file, index=False, encoding="utf-8")
import json
import pandas as  pd 
import json
from tqdm import tqdm
from cores.utils import filter_example_block
from cores.schema.category import CashCategory
from cores.schema.cashbox import CashFlowInformation
from cores.prompts.gen_time import GEN_TIME_USER, EXAMPLE
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR
from cores.output_parser.vi_pydantic import ViPydanticOutputParser
from cores.utils import filter_json_markdown
import re
from openai import AsyncOpenAI
from cores.prompts.time.time import FUNCTION_CALLING_TIME_SYSTEM_PROMPT
from cores.prompts.gen_json import DAY_MAPPING
from cores.schema.time_tool import calculate_time
import random

model_name = '/qwen-time-function-calling-v3'

client = AsyncOpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc", 
)

async def predict_time(user_prompt): 
    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": FUNCTION_CALLING_TIME_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ], 
        temperature=0
    )
    raw_context = response.choices[0].message.content
    context = filter_json_markdown(raw_context)
    context = context.replace('{{', '{').replace('}}', '}')
    
    # remove double "" in context
    context = re.sub(r'\"\"', '"', context)
    context_dict = json.loads(context)
    value = calculate_time(**context_dict)
    
    return value

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
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
        
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
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Sức khoẻ":
        if subcategory == "Khám chữa bệnh":
            model = CashCategory(health_care="Khám chữa bệnh")
        elif subcategory == "Bảo hiểm y tế":
            model = CashCategory(health_care="Bảo hiểm y tế")
        elif subcategory == "Thể thao":
            model = CashCategory(health_care="Thể thao")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
        # TODO: write more logic later
    elif category == "Dịch vụ sinh hoạt": 
        if subcategory == 'Điện': 
            model = CashCategory(living_expense='Tiền điện')
        elif subcategory == 'Nước':
            model = CashCategory(living_expense='Tiền nước')
        elif subcategory == 'Internet':
            model = CashCategory(living_expense='Tiền internet')
        elif subcategory == 'Gas':
            model = CashCategory(living_expense='Tiền gas')
        elif subcategory == 'Truyền hình':
            model = CashCategory(living_expense='Tiền truyền hình')
        elif subcategory == 'Điện thoại':
            model = CashCategory(living_expense='Tiền điện thoại')
        else: 
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
        
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
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Trang phục": 
        if subcategory == "Quần áo":
            model = CashCategory(clothing="Quần áo")
        elif subcategory == "Giầy dép":
            model = CashCategory(clothing="Giầy dép")
        elif subcategory == "Phụ kiện khác":
            model = CashCategory(clothing="Phụ kiện khác")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Hiếu hỉ":
        if subcategory == "Biếu tặng":
            model = CashCategory(gifts_donations="Biếu tặng")
        elif subcategory == "Thăm hỏi":
            model = CashCategory(gifts_donations="Thăm hỏi")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == 'Nhà cửa':
        if subcategory == "Mua sắm đồ đạc":
            model = CashCategory(household="Đồ đạc trong nhà")
        elif subcategory == "Thuê nhà":
            model = CashCategory(household="Tiền thuê nhà")
        elif subcategory == "Sửa chữa":
            model = CashCategory(household="Sửa nhà")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
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
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == 'Thú cưng':
        if subcategory == "Chó":
            model = CashCategory(pets="Chó")
        elif subcategory == "Mèo":
            model = CashCategory(pets="Mèo")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Phát triển bản thân":
        if subcategory == "Học hành":
            model = CashCategory(self_growth="Học hành")
        elif subcategory == "Giao lưu, quan hệ":
            model = CashCategory(self_growth="Xây dựng mối quan hệ")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Ngân hàng":
        if subcategory == "Phí chuyển khoản":
            model = CashCategory(bank="Phí chuyển khoản")
        elif subcategory == "Trả lãi vay":
            model = CashCategory(bank="Trả lãi vay")
        elif subcategory == "Trả nợ ngân hàng":
            model = CashCategory(bank="Trả nợ ngân hàng")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Đầu tư":
        if subcategory == "Chứng khoán":
            model = CashCategory(invest="Chứng khoán")
        elif subcategory == "Vàng":
            model = CashCategory(invest="Vàng")
        elif subcategory == "Tiền số":
            model = CashCategory(invest="Tiền số")
        elif subcategory == "Nhà đất":
            model = CashCategory(invest="Nhà đất")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "Tiết Kiệm" or category == "Tiết kiệm":
        if subcategory == "Gửi tiền tiết kiệm":
            model = CashCategory(saving="Gửi tiền tiết kiệm")
        elif subcategory == "Cho vay":
            model = CashCategory(saving="Cho vay")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    elif category == "income":
        if subcategory == "Lương":
            model = CashCategory(income="Lương")
        elif subcategory == "Thưởng":
            model = CashCategory(income="Thưởng")
        elif subcategory == "Thu hồi nợ":
            model = CashCategory(income="Thu hồi nợ")
        elif subcategory == "Kinh doanh":
            model = CashCategory(income="Kinh doanh")
        elif subcategory == "Trợ cấp":
            model = CashCategory(income="Trợ cấp")
        elif subcategory == "Rút tiết kiệm":
            model = CashCategory(income="Rút tiết kiệm")
        elif subcategory == "Bán tài sản":
            model = CashCategory(income="Bán tài sản")
        else:
            print(f"category: {category}")
            print(f"Unknown subcategory: {subcategory}")
            raise ValueError
    else:
        print(f"category: {category}")
        print(f"Unknown subcategory: {subcategory}")
        raise ValueError(f"Unknown category: {category}")
    return model

async def convert_zalo_v2(
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
        day = DAY_MAPPING[random.randint(0, 6)]
        user_str = GEN_TIME_USER.format(sentence=sentence, day=day)
        try: 
            time_dict = await predict_time(user_str)
        except Exception as e:
            print(f"Error in time generation idx {idx} : {e}")
            continue

        json_dict = {
            "spent_or_received": spent,
            "category": cash_category,
            "when": time_dict,
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
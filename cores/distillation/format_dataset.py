import pandas as pd
from tqdm import tqdm
import json
import random
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[2]))
from llama_index.core.llms import LLM

from cores.distillation.generic_generation import generic_generate
from cores.distillation.formatting_generation import formatting_generate
from cores.output_parser.vi_pydantic import ViPydanticOutputParser
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR
from cores.prompts.gen_value import GEN_VALUE_SYSTEM_PROMPT, GEN_VALUE_USER_PROMPT, GEN_VALUE_SYSTEM_WITHOUT_EXM
from cores.prompts.gen_time import GEN_TIME_SYSTEM, GEN_TIME_USER, EXAMPLE, DAY_MAPPING
from cores.utils import filter_example_block
from cores.schema.category import CashCategory
from cores.schema.time import TimeInformation
from cores.schema.cashbox import CashFlowInformation


def format_autotrain_sft(
        input_file: str,
        output_file: str
) -> None:
    df = pd.read_csv(input_file, encoding="utf-8").dropna()
    new_df = pd.DataFrame()
    for i in range(len(df)):
        sample = df.iloc[i]
        system_prompt = filter_example_block(sample["system"])
        system_prompt = system_prompt.replace("\n\n\n", "\n")
        user_prompt = sample["user"]
        assistant_prompt = sample["json"]
        combined_string = [
            {"content": system_prompt, "role": "system"},
            {"content": f"{user_prompt}", "role": "user"},
            {"content": f"{assistant_prompt}", "role": "assistant"}
        ]
        new_df = new_df._append({
            "text": combined_string
        }, ignore_index=True)

    new_df.to_csv(output_file, index=False, encoding="utf-8")


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
    return model


def change_examples_for_each_value(_value: str): 
 
    tmp = None
    value_name = None 
    million = ["triệu", 'm', "mê", "củ", "chai", "trai"]
    thousand = ["k", "cành", "nghìn", "ngàn"]
    ten_thousand = ["chục", "sịch", "xị", "sọi"]
    hundred_thousand = ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"]
    billion = ["tỷ", "tỉ", "tỏi"]
    for i in million: 
        if i in _value: 
            tmp = 10**6
            value_name = i
            break
    for i in thousand:
        if i in _value:
            tmp = 10**3
            value_name = i
            break
    
    for i in ten_thousand:
        if i in _value:
            tmp = 10**4
            value_name = i
            break
    
    for i in hundred_thousand:
        if i in _value:
            tmp = 10**5
            value_name = i
            break
    
    for i in billion:
        if i in _value:
            tmp = 10**9
            value_name = i
            break
    
    if tmp is None:
        # raise ValueError("Value not found")
        print("Change examples for each value error")
        value_name = 'chai'
        tmp = 10**6
    
    few_shot = "nộp tiền thuê mặt bằng quán cà phê tháng này tổng 3 chai 2".replace("chai", value_name)
    answer = int(3.2*tmp)
    EXAMPLE = f"\nExample:\n{few_shot}\nOutput: {answer}"  
    return GEN_VALUE_SYSTEM_WITHOUT_EXM + EXAMPLE

def convert_zalo(
        input_file: str,
        output_file: str,
        llm: LLM
) -> None:
    fp = open(input_file, 'r', encoding="utf-8")
    datas = json.load(fp)
    out_df = pd.DataFrame()

    for data in tqdm(datas):
        # sentence, type, category, subcategory, object, who, _value = \
        #     (data["content"], data["type"], data["category"],
        #      data["subcategory"], data["object"], data["who"], data["value"])
        sentence = data.get("content", None) 
        type = data.get("type", None)
        category = data.get("category", None)
        subcategory = data.get("subcategory", None)
        object = data.get("object", None)
        who = data.get("who", None)
        _value = data.get("value", None)

        if type == "chi":
            spent = True
        else:
            spent = False

        cash_category = category_to_pydantic(category, subcategory)
        cash_category = cash_category.model_dump(exclude_none=True)

        try:
            GEN_VALUE_SYSTEM_PROMPT.content = change_examples_for_each_value(_value)
            value = generic_generate(
                llm,
                GEN_VALUE_SYSTEM_PROMPT,
                GEN_VALUE_USER_PROMPT,
                prompt_kwargs=dict(
                    money=_value
                )
            )
        except Exception as e:
            print(sentence)
            print(f"Error in value generation: {e}")
            continue
            
            

        sllm = llm.as_structured_llm(TimeInformation)
        day = DAY_MAPPING[random.randint(0, 6)]
        try:
            _, user_str, time_pydantic = formatting_generate(
                sllm,
                TimeInformation,
                ViPydanticOutputParser,
                GEN_TIME_SYSTEM,
                GEN_TIME_USER,
                system_kwargs=dict(
                    example=EXAMPLE
                ),
                user_kwargs=dict(
                    sentence=sentence,
                    day=day
                ),
                parse=True
            )
        except Exception as e:
            print(sentence)
            print(f"Error in time generation: {e}")
            continue
        time_json = time_pydantic.model_dump()

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
    
    
def convert_zalo_v2(
        input_file: str,
        output_file: str,
) -> None:
    fp = open(input_file, 'r', encoding="utf-8")
    datas = json.load(fp)
    out_df = pd.DataFrame()

    for data in tqdm(datas):
        # sentence, type, category, subcategory, object, who, _value = \
        #     (data["content"], data["type"], data["category"],
        #      data["subcategory"], data["object"], data["who"], data["value"])
        sentence = data.get("content", None) 
        type = data.get("type", None)
        category = data.get("category", None)
        subcategory = data.get("subcategory", None)
        object = data.get("object", None)
        who = data.get("who", None)
        _value = data.get("value", None)

        if type == "chi":
            spent = True
        else:
            spent = False

        cash_category = category_to_pydantic(category, subcategory)
        cash_category = cash_category.model_dump(exclude_none=True)

        try:
            GEN_VALUE_SYSTEM_PROMPT.content = change_examples_for_each_value(_value)
            value = generic_generate(
                llm,
                GEN_VALUE_SYSTEM_PROMPT,
                GEN_VALUE_USER_PROMPT,
                prompt_kwargs=dict(
                    money=_value
                )
            )
        except Exception as e:
            print(sentence)
            print(f"Error in value generation: {e}")
            continue
            
            

        sllm = llm.as_structured_llm(TimeInformation)
        day = DAY_MAPPING[random.randint(0, 6)]
        try:
            _, user_str, time_pydantic = formatting_generate(
                sllm,
                TimeInformation,
                ViPydanticOutputParser,
                GEN_TIME_SYSTEM,
                GEN_TIME_USER,
                system_kwargs=dict(
                    example=EXAMPLE
                ),
                user_kwargs=dict(
                    sentence=sentence,
                    day=day
                ),
                parse=True
            )
        except Exception as e:
            print(sentence)
            print(f"Error in time generation: {e}")
            continue
        time_json = time_pydantic.model_dump()

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
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from tqdm import tqdm
from dotenv import load_dotenv

from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import ChatMessage

from cores.distillation.generic_generation import generic_generate
from cores.utils import filter_query



llm = OpenAI(
    api_key=os.getenv("openai_key"),
    model="gpt-4o-mini", 
    temperature=1.0
) # set temp = 1.0


CATEGORY_EXAMPLE_MAPPING = {
    "Chứng khoán": {
        "mờ": [
            [], # trường hợp dễ
            [
                "Chi tiền đi chơi hết 5 mờ", 
                "Đi hồ tây tiêu hết 1 mê", 
                "Mua đồ khi đi du lịch hết m 8", 
                "Chơi ở bà rịa vũng tàu hết m mốt",
                "Tiêu tiền đi chơi mờ rưỡi", 
                "Tiêu hết 6 chai 2 mươi nghìn đồng để đi chơi",
                "Hết 6 trai 8 mươi 2 để đi công viên",
                "Vào spa tiêu hết 2 củ 80 nghìn", 
                "Chi tiền chơi giải trí hết 2 mờ 2", 
                "Sang trung quốc chơi hết 20 củ 6 trăm", 
                "Vào Miền Nam chơi tháng 8 hết 8 củ tư", 
                "Chi 1 củ không trăm linh 2 nghìn để đi sang chơi ở Hải Phòng", 
                "Tiêu hết 2 củ linh tư để đi chơi game online",
                "Vào sảng chơi pocker mất 78 chai 6 cành", 
                "Đi chơi ở kangnam hết 890 chai 54 cành", 
            ] # trường hợp khó
        ]
        # "linh": [
        #     [], # trường hợp dễ
        #     [   
        #         "Chi tiền đánh quỹ hết năm mươi 3 chai 2 chục",
        #     ]
        # ]
    }
}

SYSTEM_MSG = ("You are a money manager assistant.\n"
                 "These under examples are sentences about spending money of value {value} VND for {subcategory}\n"
                 "Please generate 10 sentences that have value of {value} VND for {subcategory} similar to the examples.\n"
                 """Note that:
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
- The keywords ["tư"] represent money with value of 4
- The keywords ["mốt"] represent money with value of 1
- The keywords ["linh"] represent money with value of 0
- The keywords ["không"] represent money with value of 0
- The keywords ["trăm"] represent money with value of 100
"""
                 "EXAMPLES:\n{example}")
USER_MSG = "Similar sentences:\n"

SYSTEM_PROMPT = ChatMessage(
    role="system",
    content=SYSTEM_MSG
)
USER_PROMPT = ChatMessage(
    role="user",
    content=USER_MSG
)

for subcategory, value in CATEGORY_EXAMPLE_MAPPING.items():
    for money_value, samples in value.items():
        for i, sample in tqdm(enumerate(samples), desc=money_value):
            if sample: # tránh list rỗng
                example = "\n".join(sample)
                generated_sentences = ""
                for _ in range(50): # 500 câu
                    responses = generic_generate(
                        llm,
                        SYSTEM_PROMPT,
                        USER_PROMPT,
                        prompt_kwargs=dict(
                            value=money_value,
                            subcategory=subcategory,
                            example=example
                        )
                    )
                    responses = responses.split('\n')
                    for raw_response in responses:
                        if raw_response:
                            response = filter_query(raw_response)
                            generated_sentences += f"{response}\n"

                with open(f"data/generated/test_{subcategory}_{money_value}_{i}.txt", 'w', encoding="utf-8") as f:
                    f.write(generated_sentences)
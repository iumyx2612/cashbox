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
    "Đi chơi": {
        "sịch": [
            [
                # "Đầu tuần mua một chiếc áo mới 50 cành", 
                # "Mua một chiếc áo mới hết 10 sịch vào cuối tuần",
                # "hai hôm trước mua một chiếc áo mới 20 cành",
                # "Hôm kia mua một chiếc áo mới 30 cành",
                # "Mua đôi giày mới hết 500 cành vào cuối tuần",
                # "Mua một chiếc áo mới hết 100 cành hai hôm trước",
                "Đầu tuần đi chơi ở Hà Nội hết 50 cành",
                "Hôm qua đi chơi ở Hà Nội hết 100 cành",
                "Đi vào Đà Nẵng chơi hết 200 cành cuối tuần trước",
                "Đầu tuần đi ra Hải Phòng đi chơi biển chi phí hết 981 cành",
                
            ] # trường hợp khó
        ],
        
    }
}

SYSTEM_MSG = ("You are a money manager assistant.\n"
                 "These under examples are sentences about spending money of value {value} VND for {subcategory}\n"
                 "Please generate 10 sentences that have value of {value} VND for {subcategory} similar to the examples.\n"
                 "Note: the sentences must have similar time in the examples.\n"
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
                for _ in range(20): # 100 câu
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
                if not os.path.exists("data/generated"):
                    os.makedirs("data/generated")
                with open(f"data/generated/test_{subcategory}_{money_value}_{i}.txt", 'w', encoding="utf-8") as f:
                    f.write(generated_sentences)
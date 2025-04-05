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
    "Quần áo": {
        "loét mean hundred thousand": [
            [], # trường hợp dễ
            [
                "Ra chợ đồng xuân mua hết mờ tư",
                "Đi lên phố ra quán chị Ba mua áo mất mờ 6"
            ] # trường hợp khó
        ],
        
    }
}

SYSTEM_MSG = ("You are a money manager assistant.\n"
                 "These under examples are sentences about spending money of value {value} VND for {subcategory}\n"
                 "Please generate 10 sentences that have value of {value} VND for {subcategory} similar to the examples.\n"
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
                for _ in range(5): # 100 câu
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
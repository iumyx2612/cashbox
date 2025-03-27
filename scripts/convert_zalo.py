import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
import openai
from cores.llms.openai import OpenAI
from cores.distillation.format_dataset import convert_zalo
from tqdm import tqdm
# openai.api_key = os.getenv("openai_key")
# llm = OpenAI(model="gpt-4o-mini")

llm = OpenAI(
    api_base="http://10.0.4.239:8010/v1",
    api_key="emansieuvc", 
    model="/qwen-baseline-money-v6", 
)

save_folder = 'data_category/converted_category/Hiếu hỉ, biếu tặng'

for folder in tqdm(os.listdir("data_category/Hiếu hỉ, biếu tặng")):
    folder_path = os.path.join("data_category/Hiếu hỉ, biếu tặng", folder)
    # check if file is an folder 
    if os.path.isdir(folder_path):
        
        for files in os.listdir(folder_path):
            # check if file is done then skip 
            output_file = os.path.join(save_folder, files.replace('.json', '.csv'))
            if os.path.exists(output_file):
                print("File already exists:", output_file)
                continue
            # check if file is json
            if files.endswith(".json"):
                print("Processing file:", files)
                convert_zalo(
                    input_file=f"{folder_path}/{files}", 
                    output_file=f"{save_folder}/{files.replace('.json', '.csv')}",
                    llm=llm
                )



# # output file is csv file with header: system,user,json.
# # so we need to remove header and merge all files into one file

import pandas as pd
df = pd.DataFrame()
# for file in files:
#     df = pd.concat([df, pd.read_csv(f"data/{file.replace('.json', '.csv')}")], ignore_index=True)

# df.to_csv("data/baseline_dichvusinhhoat_dien.csv", index=False)
for file in os.listdir(save_folder):
    df = pd.concat([df, pd.read_csv(f"{save_folder}/{file}")], ignore_index=True)

df.to_csv("data_category/5xxx_concai.csv", index=False, encoding="utf-8")

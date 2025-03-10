import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
import openai
from cores.llms.openai import OpenAI
from cores.distillation.format_dataset import convert_zalo
from tqdm import tqdm
openai.api_key = os.getenv("openai_key")
llm = OpenAI(model="gpt-4o-mini")

files = ['4000_Dịch vụ sinh hoạt_Điện_1000.json', '4100_Dịch vụ sinh hoạt_Điện_300.json', '4200_Dịch vụ sinh hoạt_Điện_300.json']
for file in tqdm(files): 
    convert_zalo(
        input_file=f"data/{file}", 
        output_file=f"data/{file.replace('.json', '.csv')}",
        llm=llm
    )
    

# output file is csv file with header: system,user,json.
# so we need to remove header and merge all files into one file

import pandas as pd
df = pd.DataFrame()
for file in files:
    df = pd.concat([df, pd.read_csv(f"data/{file.replace('.json', '.csv')}")], ignore_index=True)

df.to_csv("data/baseline_dichvusinhhoat_dien.csv", index=False)
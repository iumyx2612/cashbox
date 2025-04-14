import json
import os
import sys
import asyncio
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / 'cores'))
from cores.distillation.formatting_generation_v2 import convert_zalo_v2
from tqdm import tqdm

async def process_files(folder_data, save_path):
    for file_name in tqdm(os.listdir(folder_data), total=len(os.listdir(folder_data)), desc='Processing files'):
        print(file_name)
        await convert_zalo_v2(
            input_file=os.path.join(folder_data, file_name),
            output_file=os.path.join(save_path, file_name).replace('.json', '.csv'),
        )
        

if __name__ == "__main__":
    folder_data = 'data/data_category_v2/output'
    save_path = 'data/data_category_v2/results'
    asyncio.run(process_files(folder_data, save_path))


import json
import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cores.distillation.formatting_generation_v2 import convert_zalo_v2
from tqdm import tqdm

folder_data = 'data/data_category/output'
save_path = 'data/data_category/results'
for file_name in tqdm(os.listdir(folder_data), total=len(os.listdir(folder_data)), desc='Processing files'):
    print(file_name)
    convert_zalo_v2(
        input_file=os.path.join(folder_data, file_name),
        output_file=os.path.join(save_path, file_name).replace('.json', '.csv'),
    )
    

import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / 'cores'))
print(sys.path)

from cores.distillation.format_dataset import format_autotrain_sft


format_autotrain_sft(
    'data/data_baseline_v9/baseline_time_function_calling_v1.csv', 
    'data/data_baseline_v9/baseline_time_function_calling_v1_autotrain.csv'
)
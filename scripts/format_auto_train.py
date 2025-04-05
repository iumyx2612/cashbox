import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cores.distillation.format_dataset import format_autotrain_sft


format_autotrain_sft(
    'data/data_baseline_v8/baseline_v8_category.csv', 
    'data/data_baseline_v8/baseline_v8_category_autotrain.csv'
)
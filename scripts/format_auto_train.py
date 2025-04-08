import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cores.distillation.format_dataset import format_autotrain_sft


format_autotrain_sft(
    'data/time_reasoning/function_calling_v3.csv', 
    'data/time_reasoning/function_calling_v3_autotrain.csv'
)
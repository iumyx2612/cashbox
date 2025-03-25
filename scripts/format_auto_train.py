import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cores.distillation.format_dataset import format_autotrain_sft


format_autotrain_sft(
    'data_baseline_v4/baseline_v5.csv', 
    'data_baseline_v4/baseline_v5_autotrain.csv'
)
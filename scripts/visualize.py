import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
from cores.validation.visualize import money_keyword_counter


money_keyword_counter(
    'data/data_baseline_v8/baseline_v8.csv', 
    'baseline_v8.png'
)
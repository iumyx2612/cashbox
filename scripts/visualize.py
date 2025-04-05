import os
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))
from cores.validation.visualize import money_keyword_counter


money_keyword_counter(
    '/home/hoang.minh.an/anhalu-data/learning/cashbox/data_baseline_v4/baseline_v5.csv', 
    'baseline_v5.png'
)
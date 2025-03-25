from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import os


# Đăng nhập
login(token=os.getenv('hf_token'))
model_path = '/home/hoang.minh.an/anhalu-data/learning/cashbox/qwen-baseline-money-v5'
# Tải mô hình và tokenizer (hoặc dùng mô hình của bạn)
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Đẩy lên Hugging Face
repo_name = "anhalu/qwen-baseline-money-v5"
model.push_to_hub(repo_name)
tokenizer.push_to_hub(repo_name)

print(f"Mô hình đã được đẩy lên: https://huggingface.co/{repo_name}")
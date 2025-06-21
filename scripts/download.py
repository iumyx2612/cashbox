from huggingface_hub import snapshot_download
import os

# Thiết lập token Hugging Face (phải có quyền truy cập model private)
HF_TOKEN = os.getenv("HUGGINGFACE__TOKEN")

# ID model trên Hugging Face (ví dụ: 'anhalu/qwen-baseline-time-function-calling-v3')
model_id = "anhalu/qwen-baseline-time-function-calling-v3"

# Tải model
snapshot_download(
    repo_id=model_id,
    repo_type="model",
    use_auth_token=HF_TOKEN,   # Cần dòng này nếu model là private
    local_files_only=False,    # Đảm bảo sẽ tải từ Hugging Face về
    resume_download=True       # Cho phép tiếp tục nếu trước đó bị ngắt
)

print(f"✅ Model downloaded")

# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="GSAI-ML/LLaDA-8B-Instruct", trust_remote_code=True)
pipe(messages)
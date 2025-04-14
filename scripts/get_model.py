# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="anhalu/qwen-baseline-time-function-calling-v2")
pipe(messages)
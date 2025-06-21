from transformers import AutoModelForCausalLM, AutoTokenizer


model_id = 'Qwen/Qwen3-8B'
tokenizer = AutoTokenizer.from_pretrained(model_id)
messages = [
    {
        "role": "system", "tool_name": "calculator", "content": "56088"
    },
    {
        "role": "tool",
        "tool_name": "weather_api",
        "content": "{'condition': 'rain', 'temperature': 15}",
    },
]
a = tokenizer.apply_chat_template(
    messages,
    tokenize=False
)

print(a)

from openai import OpenAI


EXAMPLE = """
giải khát công viên cùng bạn hai hôm trước tám trăm
```
{
    "absolute_date": null,
    "relative_date": -2
}
```"""

GEN_TIME_SYSTEM = """You are a money manager assistant.
Your job is to extract time information from provided sentence.
Example: {example}"""

GEN_TIME_USER = """{sentence}\nNote that today is {day}"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

user_prompt = "5 ly nước ngọt 75.000 VNĐ trong bữa tiệc vào thứ năm."

completion = client.chat.completions.create(
  model="/qwen-baseline-money-v5",
  messages=[
    {"role": "system", "content": GEN_TIME_SYSTEM.format(example=EXAMPLE)},
    {"role": "user", "content": GEN_TIME_USER.format(sentence=user_prompt, day="Thứ hai")}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
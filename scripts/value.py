from openai import OpenAI

GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""

client = OpenAI(
    base_url="http://10.0.7.50:8011/v1",
    api_key="emansieuvc"
)

user_prompt = "gửi tiết kiệm kì hạn 1 năm củ mốt"

completion = client.chat.completions.create(
  model="/qwen-money-v1",
  messages=[
    {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM},
    {"role": "user", "content": user_prompt}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
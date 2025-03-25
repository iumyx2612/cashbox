from openai import OpenAI

GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

user_prompt = "Đi đóng tiền học hết lít mốt"

completion = client.chat.completions.create(
  model="/qwen-baseline-money-v5",
  messages=[
    {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM},
    {"role": "user", "content": user_prompt}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
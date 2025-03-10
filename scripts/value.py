from openai import OpenAI

GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
Note that:
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
"""
GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="dmeman"
)


user_prompt = "2,3 me"

completion = client.chat.completions.create(
  model="models/qwen-baseline-money-v1",
  messages=[
    {"role": "system", "content": GEN_VALUE_SYSTEM_WITHOUT_EXM},
    {"role": "user", "content": user_prompt}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
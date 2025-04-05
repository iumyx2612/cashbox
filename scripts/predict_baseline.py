from openai import OpenAI

DAY_MAPPING = {
    0: "Thứ hai",
    1: "Thứ ba",
    2: "Thứ tư",
    3: "Thứ năm",
    4: "Thứ sáu",
    5: "Thứ bảy",
    6: "Chủ nhật"
}

EXAMPLE = """giải khát công viên cùng bạn hai hôm trước tám trăm
```json
{
    "spent_or_received": true,
    "category": {
        "food": "Đồ uống"
    },
    "when": {
        "absolute_date": null,
        "relative_date": -2
    },
    "object": "giải khát",
    "who": "bạn",
    "value": 800000
}
```"""

GEN_FORMAT_SYSTEM_STR = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user
Example:
{example}"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

sentence = "4,5 lít đi chợ online hôm thứ năm."
day = "Thứ hai"
GEN_FORMAT_USER_STR = """{sentence}\nNote that today is {day}"""


completion = client.chat.completions.create(
  model="/qwen-baseline-money-v5",
  messages=[
    {"role": "system", "content": GEN_FORMAT_SYSTEM_STR.format(example=EXAMPLE)},
    {"role": "user", "content": GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
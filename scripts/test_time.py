from openai import OpenAI


SYSTEM_MSG = """You are a money manager assistant.
Your job is to extract time information in JSON from provided sentence.

Here's a JSON schema to follow:
{{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to mentioned day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
Remember to think step by step
"""

GEN_TIME_USER = """{sentence}\nNote that today is {day}"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="dmeman"
)

user_prompt = "5 ly nước ngọt 75.000 VNĐ trong bữa tiệc vào thứ năm."
sentence_2 = 'cuối tháng lương tháng 73 triệu.'

completion = client.chat.completions.create(
  model="qwen-reasoning-time-v1",
  messages=[
    {"role": "system", "content": SYSTEM_MSG},
    {"role": "user", "content": GEN_TIME_USER.format(sentence=sentence_2, day="Thứ hai")}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    
from datetime import datetime

from llama_index.core.prompts import ChatPromptTemplate, ChatMessage, MessageRole


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
Note that today is {day}
Please ALWAYS response in Python JSON format and in the same language as user
Example:
{example}"""

GEN_FORMAT_USER_STR = """{sentence}"""

GEN_FORMAT_SYSTEM_PROMPT = ChatMessage(
    content=GEN_FORMAT_SYSTEM_STR,
    role=MessageRole.SYSTEM
)

GEN_FORMAT_USER_PROMPT = ChatMessage(
    content=GEN_FORMAT_USER_STR,
    role=MessageRole.USER
)

GEN_FORMAT_PROMPT = ChatPromptTemplate([
    GEN_FORMAT_SYSTEM_PROMPT, GEN_FORMAT_USER_PROMPT
])
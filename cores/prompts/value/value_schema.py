import re

from llama_index.core.prompts import ChatMessage, ChatPromptTemplate


EXAMPLES = {
    ("tỷ", "tỉ", "tỏi"): "nộp tiền thuê mặt bằng tháng này tổng 3 tỷ 2\n"
                         "Output: 3200000000",
    ("triệu", 'm', "mê", "củ", "chai", "trai"): "nộp tiền thuê mặt bằng tháng này tổng 3 củ 2\n"
                                                "Output: 3200000",
    ("trăm", "lít", "loét", "lốp", "lip", "líp", "list"):
        "nộp tiền thuê mặt bằng tháng này tổng 3 loét 2\n"
        "Output: 320000",
    ("chục", "sịch", "xị", "sọi"): "nộp tiền thuê mặt bằng tháng này tổng 3 sọi 2\n"
                                   "Output: 32000",
    ("k", "cành", "nghìn", "ngàn"): "nộp tiền thuê mặt bằng quán cà phê tháng này tổng 3 ngàn 2\n"
                                    "Output: 3200"
}


GEN_VALUE_SCHEMA_SYSTEM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
Note that:
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
Example:
{example}
"""

GEN_VALUE_SCHEMA_USER = """{sentence}"""

GEN_VALUE_SYSTEM_PROMPT = ChatMessage(
    role="system",
    content=GEN_VALUE_SCHEMA_SYSTEM
)

GEN_VALUE_USER_PROMPT = ChatMessage(
    role="user",
    content=GEN_VALUE_SCHEMA_USER
)

GEN_VALUE_PROMPT = ChatPromptTemplate(
    [GEN_VALUE_SYSTEM_PROMPT, GEN_VALUE_USER_PROMPT]
)


def get_example(query: str) -> str:
    for keywords, example in EXAMPLES.items():
        for kw in keywords:
            pattern = r'\b{kw}\b'.format(kw=kw)

            matches = re.findall(pattern, query)

            if matches:
                return example

    return ("nộp tiền thuê mặt bằng tháng này tổng 3 loét 2\n"
            "Output: 320000")
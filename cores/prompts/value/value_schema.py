from llama_index.core.prompts import ChatMessage, ChatPromptTemplate


GEN_VALUE_SCHEMA_SYSTEM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
Note that:
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
Example:
nộp tiền thuê mặt bằng quán cà phê tháng này tổng 3 ngàn 2
Output: 3200
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
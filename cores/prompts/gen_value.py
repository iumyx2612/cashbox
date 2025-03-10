from llama_index.core.prompts import ChatMessage, ChatPromptTemplate


GEN_VALUE_SYSTEM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
Note that:
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
Example:
nộp tiền thuê mặt bằng quán cà phê tháng này tổng 3 chai 2
Output: 3200000
"""

GEN_VALUE_USER = """{money}"""

GEN_VALUE_SYSTEM_PROMPT = ChatMessage(
    role="system",
    content=GEN_VALUE_SYSTEM
)

GEN_VALUE_USER_PROMPT = ChatMessage(
    role="user",
    content=GEN_VALUE_USER
)

GEN_VALUE_PROMPT = ChatPromptTemplate(
    [GEN_VALUE_SYSTEM_PROMPT, GEN_VALUE_USER_PROMPT]
)

GEN_VALUE_SYSTEM_WITHOUT_EXM = """You're an money manager assistant.
Your job is to find and convert textual money string into integer money string
Note that:
- The keywords ["triệu", 'm', "mê", "củ", "chai", "trai"] represent money with value of million
- The keywords ["trăm", "lít", "loét", "lốp", "lip", "líp", "list"] represent money with value of hundred thousand
- The keywords ["chục", "sịch", "xị", "sọi"] represent money with value of ten thousand
- The keywords ["k", "cành", "nghìn", "ngàn"] represent money with value of thousand
- The keywords ["tỷ", "tỉ", "tỏi"] represent money with value of billion
"""
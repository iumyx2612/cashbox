from llama_index.core.prompts import ChatMessage, ChatPromptTemplate


GEN_VALUE_SYSTEM = """You're an money manager assistant.
Your job is to convert textual money string into integer money string
Example:
user: 5 triệu 9 trăm nghìn
assistant: 5900000
================
user: 2,5 lít
assistant: 250000
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
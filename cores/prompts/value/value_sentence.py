from llama_index.core.prompts import ChatMessage


GEN_VALUE_SENTENCE_SYSTEM = """You're an money manager assistant.
Your job is to generate 10 similar sentences to the examples about using money.
Note that these keywords {key_words} refer to the money value of {value}
# Example:\n{examples}
"""

GEN_VALUE_SENTENCE_USER = """Similar sentences:\n"""

GEN_VALUE_SENTENCE_SYSTEM_PROMPT = ChatMessage(
    content=GEN_VALUE_SENTENCE_SYSTEM,
    role="system"
)

GEN_VALUE_SENTENCE_USER_PROMPT = ChatMessage(
    content=GEN_VALUE_SENTENCE_USER,
    role="user"
)
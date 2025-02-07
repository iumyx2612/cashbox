from llama_index.core.prompts import ChatMessage, MessageRole, ChatPromptTemplate


GEN_SENTENCES_SYSTEM = ChatMessage(
    content="Given a set of example sentences that describe how the money was spent.\n"
            "Please generate 10 sentences that are similar to the examples\n"
            "# Examples:\n{examples}",
    role=MessageRole.SYSTEM
)

GEN_SENTENCES_USER = ChatMessage(
    content="# Similar sentences:\n",
    role=MessageRole.USER
)

GEN_SENTENCES_PROMPT = ChatPromptTemplate([
    GEN_SENTENCES_SYSTEM, GEN_SENTENCES_USER
])
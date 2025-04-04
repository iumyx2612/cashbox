from llama_index.core.prompts import ChatMessage


EXAMPLE = ("- 5 củ 200.000 đậu xe máy ở nhà thứ 6\n"
           "- trà đá ở Hồ Gươm 15k hôm thứ 3")

TIME_SENTENCE_SYSTEM = \
    ("You are an expert in Vietnamese Language\n"
     "These under examples are sentence about spending money on certain day "
     "of the week\n"
     "Your job is to generate 10 sentences about spending money on {day}\n"
     "{day} can be written in text or number\n"
     "Example:\n"
     "{example}")

TIME_SENTENCE_USER = "Similar sentences:\n"

TIME_SENTENCE_SYSTEM_PROMPT = ChatMessage(
    content=TIME_SENTENCE_SYSTEM,
    role="system"
)

TIME_SENTENCE_USER_PROMPT = ChatMessage(
    content=TIME_SENTENCE_USER,
    role="user"
)

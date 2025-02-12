from typing import Union, Optional

from llama_index.core.llms import LLM
from llama_index.core.prompts import ChatMessage, ChatPromptTemplate


def generic_generate(
        llm: LLM,
        system_prompt: Union[ChatMessage, str],
        user_prompt: Union[ChatMessage, str],
        system_kwargs: Optional[dict] = None,
        user_kwargs: Optional[dict] = None,
        prompt_kwargs: Optional[dict] = None
) -> str:
    if prompt_kwargs and (user_kwargs or system_kwargs):
        raise AssertionError("Detect both `prompt_kwargs` and user_kwargs or system_kwargs")
    if system_kwargs and not isinstance(system_prompt, str):
        raise AssertionError
    if user_kwargs and not isinstance(user_prompt, str):
        raise AssertionError

    if prompt_kwargs and isinstance(system_prompt, ChatMessage):
        prompt = ChatPromptTemplate([system_prompt, user_prompt])
        response = llm.predict(prompt, **prompt_kwargs)

        return response

    if system_kwargs:
        system_prompt = system_prompt.format(**system_kwargs)
    if user_kwargs:
        user_prompt = user_prompt.format(**user_kwargs)

    system_prompt = ChatMessage(content=system_prompt, role="system")
    user_prompt = ChatMessage(content=user_prompt, role="user")
    prompt = ChatPromptTemplate([system_prompt, user_prompt])
    response = llm.predict(prompt, **prompt_kwargs)

    return response
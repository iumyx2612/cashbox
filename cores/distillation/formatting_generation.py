from typing import Optional, Tuple, Type

from llama_index.core.llms import LLM
from llama_index.core.bridge.pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.prompts import ChatMessage


def formatting_generate(
        llm: LLM,
        pydantic_model: Type[BaseModel],
        output_parser_cls: Type[PydanticOutputParser],
        system_prompt: str,
        user_prompt: str,
        system_kwargs: Optional[dict] = None,
        user_kwargs: Optional[dict] = None,
) -> Tuple[str, str, str]:
    if system_kwargs and not isinstance(system_prompt, str):
        raise AssertionError
    if user_kwargs and not isinstance(user_prompt, str):
        raise AssertionError

    if system_kwargs:
        system_prompt = system_prompt.format(**system_kwargs)
    if user_kwargs:
        user_prompt = user_prompt.format(**user_kwargs)

    system_prompt = ChatMessage(content=system_prompt, role="system")
    user_prompt = ChatMessage(content=user_prompt, role="user")

    output_parser = output_parser_cls(pydantic_model)
    format_str = output_parser.format_string

    sllm = llm.as_structured_llm(pydantic_model)
    response = sllm.chat([system_prompt, user_prompt])

    system_str = f"{system_prompt.content}\n{format_str}"
    user_str = user_prompt.content
    output_format = response.message.content

    return (system_str, user_str, output_format)
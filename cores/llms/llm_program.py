from typing import Optional, Dict, Any, Union
from llama_index.core.bridge.pydantic import BaseModel

from llama_index.core.program.llm_program import (
    LLMTextCompletionProgram as LITextCompletionProgram
)


class LLMTextCompletionProgram(LITextCompletionProgram):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(
            self,
            llm_kwargs: Optional[Dict[str, Any]] = None,
            parse: bool = True,
            *args: Any,
            **kwargs: Any,
    ) -> Union[BaseModel, str]:
        _parse = llm_kwargs.pop("parse", None)
        parse = _parse if _parse is not None else parse
        llm_kwargs = llm_kwargs or {}
        if self._llm.metadata.is_chat_model:
            messages = self._prompt.format_messages(llm=self._llm, **kwargs)
            messages = self._llm._extend_messages(messages)
            chat_response = self._llm.chat(messages, **llm_kwargs)

            raw_output = chat_response.message.content or ""
        else:
            formatted_prompt = self._prompt.format(llm=self._llm, **kwargs)

            response = self._llm.complete(formatted_prompt, **llm_kwargs)

            raw_output = response.text
        if parse:
            output = self._output_parser.parse(raw_output)
            if not isinstance(output, self._output_cls):
                raise ValueError(
                    f"Output parser returned {type(output)} but expected {self._output_cls}"
                )
        else:
            output = raw_output

        return output
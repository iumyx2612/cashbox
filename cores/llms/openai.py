from typing import Type, Optional, Dict, Any

from llama_index.core.bridge.pydantic import BaseModel
from llama_index.llms.openai.base import (
    LLMMetadata,
    openai_modelname_to_contextsize,
    is_chat_model,
    O1_MODELS
)
from llama_index.llms.openai import OpenAI as LIOpenAI
from llama_index.core.prompts import MessageRole
from llama_index.core.prompts import PromptTemplate
from llama_index.core.output_parsers import PydanticOutputParser


class OpenAI(LIOpenAI):
    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=1600, # Fixed for Finetuned Qwen. Doesn't matter anw
            num_output=self.max_tokens or -1,
            is_chat_model=True,
            is_function_calling_model=False,
            model_name=self.model,
            # TODO: Temp for O1 beta
            system_role=MessageRole.USER
            if self.model in O1_MODELS
            else MessageRole.SYSTEM,
        )

    def as_structured_llm(self, output_cls, **kwargs):
        from .structured_llm import StructuredLLM

        return StructuredLLM(llm=self, output_cls=output_cls, **kwargs)

    def structured_predict(
            self,
            output_cls: Type[BaseModel],
            prompt: PromptTemplate,
            parse: bool = True,
            llm_kwargs: Optional[Dict[str, Any]] = None,
            **prompt_args: Any,
    ) -> BaseModel:
        from .llm_program import LLMTextCompletionProgram
        from ..output_parser.vi_pydantic import ViPydanticOutputParser
        program = LLMTextCompletionProgram.from_defaults(
            output_parser=ViPydanticOutputParser(output_cls=output_cls),
            llm=self,
            prompt=prompt
        )

        result = program(llm_kwargs=llm_kwargs, parse=parse, **prompt_args)
        return result
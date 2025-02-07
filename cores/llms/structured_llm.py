from typing import Sequence, Any

from llama_index.core.llms.structured_llm import (
    StructuredLLM as LIStructured,
    ChatMessage,
    ChatResponse,
    ChatPromptTemplate,
    MessageRole
)

class StructuredLLM(LIStructured):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def chat(self,
             messages: Sequence[ChatMessage],
             parse: bool = True,
             **kwargs: Any) -> ChatResponse:
        """Chat endpoint for LLM."""
        # TODO:

        # NOTE: we are wrapping existing messages in a ChatPromptTemplate to
        # make this work with our FunctionCallingProgram, even though
        # the messages don't technically have any variables (they are already formatted)

        chat_prompt = ChatPromptTemplate(message_templates=messages)

        output = self.llm.structured_predict(
            output_cls=self.output_cls,
            prompt=chat_prompt,
            parse=parse,
            llm_kwargs=kwargs
        )
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT, content=output.model_dump_json() if parse else output
            ),
            raw=output,
        )
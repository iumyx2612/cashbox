from typing import Optional, Literal

from llama_index.core.bridge.pydantic import BaseModel, Field

from .time import TimeInformation
from .category import CashCategory


class CashFlowInformation(BaseModel):
    spent_or_received: bool = Field(
        description="Is the money spent on things or received from another. True for spent, False for received"
    )
    category: CashCategory
    when: TimeInformation
    object: str = Field(
        description="The object that affects the money mentioned in the sentence."
    )
    who: Optional[str] = Field(
        default=None,
        description="The person mentioned in the sentence"
    )
    value: int = Field(
        description="Amount of money"
    )
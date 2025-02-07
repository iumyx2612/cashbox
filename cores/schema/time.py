from typing import Optional
from llama_index.core.bridge.pydantic import BaseModel, Field


class TimeInformation(BaseModel):
    absolute_date: Optional[str] = Field(
        default=None,
        description="Date in dd-mm format. Null if specific date is not mentioned"
    )
    relative_date: int = Field(
        default=0,
        description="How many days from today to said day. Use default value if not mentioned",
        le=0
    )
from pydantic import BaseModel 
from typing import Optional

class HuggingfaceSettings(BaseModel):
    username: Optional[str] = None
    token: Optional[str] = None

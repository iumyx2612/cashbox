from pydantic import BaseModel 


class TimeSettings(BaseModel): 
    base_url: str
    api_key: str
    port: str
    model_name: str
from pydantic import BaseModel 


class BaselineSettings(BaseModel): 
    base_url: str
    port: str
    api_key: str
    model_name: str
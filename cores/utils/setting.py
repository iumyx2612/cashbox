from dotenv import find_dotenv 
from dotenv import load_dotenv 
from pydantic_settings import BaseSettings

from .BaselineSettings import BaselineSettings 
from .TimeSettings import TimeSettings
from .HuggingfaceSettings import HuggingfaceSettings

load_dotenv(find_dotenv('.env'), override=True) 



class Settings(BaseSettings): 
    baseline: BaselineSettings
    time: TimeSettings 
    huggingface: HuggingfaceSettings

    class Config:
        env_nested_delimiter = '__'

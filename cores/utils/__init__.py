from dotenv import find_dotenv 
from dotenv import load_dotenv 


from .utils import filter_query, filter_example_block, filter_json_markdown_anywhere, filter_json_markdown
from .logging import setup_logging, get_logger
from .setting import Settings 


def get_settings():
    """
    Load settings from the environment variables.
    """
    load_dotenv(find_dotenv('.env'), override=True) 
    settings = Settings()
    return settings


import re
from llama_index.core.output_parsers.utils import extract_json_str as filter_json_markdown
import time
from functools import wraps


def filter_query(query: str) -> str:
    """ Remove punctuation at the beginning of sentence. Useful
    when using with generic_generate """
    query = re.sub(r"^\d+\.\s*|-+\s*|\n", "", query)
    query = query.strip()
    return query


def filter_example_block(query: str) -> str:
    return re.sub(r'Example:.*?```.*?```', '', query, flags=re.DOTALL).strip()


# def filter_json_markdown(query: str) -> str:
#     match = re.search(r'^```json\n(.*?)\n```$', query, re.DOTALL)
#     return match.group(1) if match else ""
# def filter_json_markdown(query: str) -> str:
#     match = re.search(r'^```json\n(.*?)\n```$', query, re.DOTALL)
#     return match.group(1) if match else ""


def filter_json_markdown_anywhere(query: str) -> str:
    match = re.search(r'```json\n(.*?)\n```', query, re.DOTALL)
    return match.group(1) if match else ""


def time_decorator(predictor_name: str):
    """
    Decorator to measure the runtime of a predictor and update the Node's running_time.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            node = await func(*args, **kwargs)
            end_time = time.time()
            runtime = end_time - start_time
            if node and hasattr(node, 'running_time'):
                node.running_time[predictor_name] = runtime
            return node
        return wrapper
    return decorator
import json
import re

from cores.utils import filter_json_markdown


def fix_json_string(
        json_str: str
) -> str:
    corrected_str = re.sub(r'^\{+', '{', json_str)  # Replace multiple leading {
    corrected_str = re.sub(r'\}+$', '}', corrected_str)  # Replace multiple trailing }
    return corrected_str


def get_noted_day(
        query: str
) -> str:
    """The query usually Note that today is x"""
    match = re.search(r'Note that today is (.+)', query)
    return match.group(1) if match else ""


def get_mentioned_day(
    query: str
) -> str:
    if "chủ nhật" in query.lower():
        return "chủ nhật"
    match = re.search(r'(?i)thứ\s+(\S+)', query)
    return re.sub(r'\W', '', match.group(1)) if match else ""


def filter_time(
        json_str: str
) -> dict:
    json_str = filter_json_markdown(json_str)
    json_dict = json.loads(json_str)
    time = json_dict["when"]
    return time

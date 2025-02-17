import re


def filter_query(query: str) -> str:
    query = re.sub(r"^\d+\.\s*|-+\s*|\n", "", query)
    query = query.strip()
    return query


def filter_example_block(query: str) -> str:
    return re.sub(r'Example:.*?```.*?```', '', query, flags=re.DOTALL).strip()


def filter_json_markdown(query: str) -> str:
    match = re.search(r'^```json\n(.*?)\n```$', query, re.DOTALL)
    return match.group(1) if match else ""
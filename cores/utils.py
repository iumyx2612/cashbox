import re


def filter_query(query: str) -> str:
    query = re.sub(r"^\d+\.\s*|-+\s*|\n", "", query)
    query = query.strip()
    return query
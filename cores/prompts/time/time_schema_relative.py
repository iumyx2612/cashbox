TIME_SCHEMA_RELATIVE_SYSTEM = """You understand correlation of time for days in a week.
Your job is to calculate the time difference between 2 day
Please follow the instructions below:
1. Simply generate a step-by-step reasoning.
2. Response in Python JSON format
Please write "Reasoning:\\n<reasoning>" to output your reasoning without any additional information
And write "Answer:\\n<answer>" to output your JSON answer

Here's a JSON schema to follow:
{{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to mentioned day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}

Here is an example for your reference:
{example}
"""

TIME_SCHEMA_RELATIVE_USER = "{sentence}"

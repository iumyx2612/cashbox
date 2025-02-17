from .gen_json import DAY_MAPPING as iDAY_MAPPING


DAY_MAPPING = iDAY_MAPPING

EXAMPLE = """
giải khát công viên cùng bạn hai hôm trước tám trăm
```
{
    "absolute_date": null,
    "relative_date": -2
}
```"""

GEN_TIME_SYSTEM = """You are a money manager assistant.
Your job is to extract time information from provided sentence.
Example: {example}"""

GEN_TIME_USER = """{sentence}\nNote that today is {day}"""
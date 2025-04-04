from typing import Literal

from llama_index.core.tools import FunctionTool
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.agent.react.formatter import get_react_tool_descriptions
from llama_index.core.tools.calling import call_tool_with_selection
from llama_index.core.prompts import ChatMessage


TIME_EXAMPLE_SYSTEM = ("Your job is to find mentioned date and today in provided sentence"
                       "and use as inputs for below tool\n"
                       "{tool_desc}")

TIME_EXAMPLE_USER = "{sentence}"


DATE_ARRAY = [
    "Thứ hai",
    "Thứ ba",
    "Thứ tư",
    "Thứ năm",
    "Thứ sáu",
    "Thứ bảy",
    "Chủ Nhật"
]


def make_example_tool(
        mentioned_date: Literal[
            "Thứ hai", "Thứ ba", "Thứ tư",
            "Thứ năm", "Thứ sáu", "Thứ bảy",
            "Chủ Nhật"
        ],
        today: Literal[
            "Thứ hai", "Thứ ba", "Thứ tư",
            "Thứ năm", "Thứ sáu", "Thứ bảy",
            "Chủ Nhật"
        ]
) -> str:
    sample = (f"user: Uống trà sữa hết 200k vào {mentioned_date}\n"
              "Note that today is {today}").format(
        mentioned_date=mentioned_date,
        today=today
    )
    example_str = sample + "\n\n" + "Reasoning:\n"

    reasoning_1 = f"1. Today is {today}, mentioned date is {mentioned_date}"

    if today == mentioned_date:
        reasoning_2 = f"2. Since both today and the mentioned date are the same, there is no time difference."
        reasoning_3 = f"3. Therefore, the relative date is 0 days."
        answer = """Answer:
```json
{
    "absolute_date": null,
    "relative_date": 0
}
```"""
        example_str += f"{reasoning_1}\n{reasoning_2}\n{reasoning_3}\n\n{answer}"
        return example_str

    reasoning_2 = f"2. Traverse time backward from {today} to {mentioned_date}: "

    index = DATE_ARRAY.index(today)
    date_arr = []
    end_date = ""
    while end_date != mentioned_date:
        index -= 1
        end_date = DATE_ARRAY[index]
        date_arr.append(end_date)

    reasoning_3 = f"3. Based on step 2, there are {len(date_arr)} days"
    date_arr_str = ""
    for date in date_arr:
        date_arr_str += f"{date}, "

    answer_json = \
    """
```json
{{
    "absolute_date": null,
    "relative_date": {ans}
}}
```
    """.format(
        ans=f"-{int(len(date_arr))}"
    )
    answer = "Answer:" + answer_json

    example_str += f"{reasoning_1}\n{reasoning_2}{date_arr_str}\n{reasoning_3}\n\n{answer}"

    return example_str


def make_example(
        llm: FunctionCallingLLM,
        sentence: str
) -> str:
    example_tool = FunctionTool.from_defaults(
        fn=make_example_tool
    )
    tool_response = llm.chat_with_tools(
        [example_tool],
        ChatMessage(
            content=TIME_EXAMPLE_USER.format(
                sentence=sentence
            ),
            role="user"
        ),
        [
            ChatMessage(
                content=TIME_EXAMPLE_SYSTEM.format(
                    tool_desc=get_react_tool_descriptions([example_tool])[0]
                ),
                role="system"
            )
        ]
    )
    tool_call = llm.get_tool_calls_from_response(
        tool_response, error_on_no_tool_call=False
    )[0]
    example = call_tool_with_selection(
        tool_call, [example_tool]
    )
    example = str(example)

    return example
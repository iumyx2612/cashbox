import json
import os
import pandas as pd
import sys
from pathlib import Path    
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
from tqdm import tqdm

from llama_index.core.prompts import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.calling import call_tool_with_selection

from cores.llms.openai import OpenAI
from cores.schema.time_tool import calculate_time
from cores.prompts.time.time_function import TIME_FUNCTION_SYSTEM, TIME_FUNCTION_USER


load_dotenv()


SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to provide arguments for the tool below to extract and calculate time information
Note you must use the tool to calculate the time difference between mentioned date and today.

Tool schema:
{'name': 'calculate_time', 'description': 'calculate_time(today: Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\'], mentioned_date: Optional[Literal[\'Thứ hai\', \'Thứ ba\', \'Thứ tư\', \'Thứ năm\', \'Thứ sáu\', \'Thứ bảy\', \'Chủ Nhật\', \'Undefine\']], week: Optional[int] = 0, absolute_date: Optional[str] = None, relative_date: Optional[int] = None)', 'parameters': {'properties': {'today': {'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật'], 'title': 'Today', 'type': 'string'}, 'mentioned_date': {'anyOf': [{'enum': ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ Nhật', 'Undefine'], 'type': 'string'}, {'type': 'null'}], 'title': 'Mentioned Date'}, 'week': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 0, 'title': 'Week'}, 'absolute_date': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Absolute Date'}, 'relative_date': {'anyOf': [{'type': 'int'}, {'type': 'null'}], 'default': None, 'title': 'Relative Date'}}, 'required': ['today', 'mentioned_date'], 'type': 'object'}} 
"""
llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0,
    strict=True, 
    api_key=os.getenv("openai_key"),
)

files = [
    "data_time_reasoning.csv",
    'merged_time_absolute.csv',
    # "time_sentences_2_5.csv",
    # "time_sentences_1_2.csv",
    # "time_sentences_2_2.csv",
    # "time_sentences_3_2.csv",
    # "time_sentences_4_2.csv",
    # "time_sentences_5_2.csv",
    # "time_sentences_6_2.csv"
]

tool = FunctionTool.from_defaults(
    fn=calculate_time
)


for file in tqdm(files):
    out_df = pd.DataFrame()
    file_path = f"data/time_reasoning/{file}"
    samples = pd.read_csv(file_path, encoding='utf-8')["user"]
    print(f"Processing {file_path} with {len(samples)} samples") 
    for index, sample in tqdm(enumerate(samples), desc=file, total=len(samples)):
        tool_kwargs_base = json.loads("""{
            "today": "Thứ hai",
            "mentioned_date": "Thứ hai",
            "week": 0,
            "absolute_date": null,
            "relative_date": null
        }""")

        try:
            response = llm.chat_with_tools(
                [tool],
                ChatMessage(
                    content=TIME_FUNCTION_USER.format(
                        sentence=sample
                    ),
                    role="user"
                ),
                [
                    ChatMessage(
                        content=TIME_FUNCTION_SYSTEM,
                        role="system"
                    )
                ]
            )

            tool_call = llm.get_tool_calls_from_response(
                response, error_on_no_tool_call=False
            )[0]

            tool_kwargs = tool_call.tool_kwargs

            for arg, val in tool_kwargs_base.items():
                for llm_arg, llm_val in tool_kwargs.items():
                    if arg == llm_arg:
                        tool_kwargs_base[arg] = llm_val
                        break

            tool_kwargs_json = json.dumps(
                tool_kwargs_base, ensure_ascii=False, indent=4
            )

            out_df = out_df._append({
                "system": SYSTEM_PROMPT,
                "user": sample,
                "json": f"```json\n{tool_kwargs_json}\n```",
                "answer": call_tool_with_selection(
                    tool_call, [tool]
                ).raw_output
            }, ignore_index=True)
        except:
            print(f"Error in {file}: sample idx {index}: {sample}")
            pass
        # break 
        if index % 500 == 0 and index > 0:
            out_df.to_csv(f"data/time_reasoning/function_calling/{index}_{file}", index=False)
            out_df = pd.DataFrame()
            
    out_df.to_csv(f"data/time_reasoning/function_calling/last_{file}", index=False)
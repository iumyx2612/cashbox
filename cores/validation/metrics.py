from typing import Union
from tqdm import tqdm
import pandas as pd
import json

from llama_index.core.prompts import ChatMessage

from cores.llms.structured_llm import StructuredLLM
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, EXAMPLE
from cores.utils import filter_example_block, filter_json_markdown


def time_accuracy(
        pred_json: Union[str, dict],
        gt_json: Union[str, dict]
) -> float:
    if isinstance(pred_json, str):
        pred_json: dict = json.loads(pred_json)
    if isinstance(gt_json, str):
        gt_json: dict = json.loads(gt_json)

    p_absolute_time, p_relative_time = pred_json["absolute_date"], pred_json["relative_date"]
    gt_absolute_time, gt_relative_time = gt_json["absolute_date"], gt_json["relative_date"]

    if gt_absolute_time == p_absolute_time and gt_absolute_time != None:
        return 1

    elif gt_relative_time == p_relative_time and gt_relative_time != None:
        return 1
    else:
        return 0


def accuracy(
        pred_json,
        gt_json
) -> float:
    # Slowest accuracy calculator ever
    pred_dict: dict = json.loads(pred_json)
    gt_dict: dict = json.loads(gt_json)

    total_items = len(gt_dict.items())
    acc = total_items

    keys = ["spent_or_received", "category", "when", "object", "who", "value"]

    # TODO: Stupid, need fix
    for k in keys:
        pred_v = pred_dict.get(k, None)
        gt_v = gt_dict.get(k, None)

        # TODO: Can remove this later when better training set
        if k == "value":
            pred_v = int(pred_v)

        if isinstance(gt_v, str):
            if pred_v.lower() != gt_v.lower():
                acc -= 1
        else:
            if pred_v != gt_v:
                acc -= 1

    acc = acc / total_items

    return acc


def validate_model(
        llm: StructuredLLM,
        input_file: str,
        output_file: str
) -> None:
    test_df = pd.read_csv(input_file)

    out_df = pd.DataFrame()
    total_acc = 0
    total_samples = len(test_df)

    system_str = GEN_FORMAT_SYSTEM_STR.format(example=EXAMPLE)
    system_str = filter_example_block(system_str)

    for i in tqdm(range(len(test_df))):
        test_sample = test_df.iloc[i]
        user_str = test_sample["user"]
        gt_json = test_sample["json"]
        gt_json = filter_json_markdown(gt_json)

        system_prompt = ChatMessage(
            content=system_str,
            role="system"
        )
        user_prompt = ChatMessage(
            content=user_str,
            role="user"
        )

        response = llm.chat(
            [system_prompt, user_prompt], parse=False
        )
        pred_json = filter_json_markdown(response.raw)

        acc = accuracy(pred_json, gt_json)
        total_acc += acc

        out_df = out_df._append({
            "system": system_str,
            "user": user_str,
            "json": response.raw
        }, ignore_index=True)

    print(f">>> Total accuracy: {total_acc / total_samples}")
    out_df.to_csv(output_file, index=False)
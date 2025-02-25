from tqdm import tqdm
import pandas as pd

from llama_index.core.prompts import ChatMessage

from cores.llms.structured_llm import StructuredLLM
from cores.prompts.gen_json import GEN_FORMAT_SYSTEM_STR, EXAMPLE
from cores.utils import filter_example_block, filter_json_markdown
from .metrics import accuracy


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
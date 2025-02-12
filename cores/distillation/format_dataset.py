import pandas as pd

from ..utils import filter_example_block


def format_autotrain_sft(
        input_file: str,
        output_file: str
) -> None:
    df = pd.read_csv(input_file, encoding="utf-8")
    new_df = pd.DataFrame()
    for i in range(len(df)):
        sample = df.iloc[i]
        system_prompt = filter_example_block(sample["system"])
        user_prompt = sample["user"]
        assistant_prompt = sample["json"]
        combined_string = [
            {"content": system_prompt, "role": "system"},
            {"content": f"{user_prompt}", "role": "user"},
            {"content": f"{assistant_prompt}", "role": "assistant"}
        ]
        new_df = new_df._append({
            "text": combined_string
        }, ignore_index=True)

    new_df.to_csv(output_file, index=False, encoding="utf-8")
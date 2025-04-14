import asyncio
from openai import AsyncOpenAI
import pandas as pd
import json
import os
from llama_index.core.output_parsers.utils import extract_json_str as filter_json_markdown
from tqdm import tqdm

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

MENTIONED_DATE_EXTRACT_SYSTEM_PROMPT = """You are provided with an input sentence in Vietnamese that contains a reference to time. Your task is to extract and output the day of the week mentioned in the sentence. The valid days of the week are strictly limited to the following: Thứ hai, Thứ ba, Thứ tư, Thứ năm, Thứ sáu, Thứ bảy, Chủ Nhật.

Follow these rules:

1. Weekend Special Case:
- If the sentence includes the phrase "cuối tuần" without any accompanying specific weekday, output "Chủ Nhật".
- If "cuối tuần" is mentioned along with a specific weekday from the list, output the specific weekday mentioned.

2. Beginning of the Week Special Case:
- If the sentence includes the phrase "đầu tuần" without any accompanying specific weekday, output "Thứ hai".
- If "đầu tuần" is mentioned along with a specific weekday from the list, output the specific weekday mentioned.

3. No Day Specified:
- If the sentence does not mention any day of the week as per the list, output "Undefine".

REMEMBER, your output must be exactly one of the following: Thứ hai, Thứ ba, Thứ tư, Thứ năm, Thứ sáu, Thứ bảy, Chủ Nhật, or Undefine.
"""


async def predict_time_async(sentence: str) -> str:
    """Predict the time of the sentence asynchronously"""
    sentences = [
        'Đặt phòng khách sạn 1 triệu cho cuối tuần thứ 7.',
        'Uống cà phê tại quán quen hết 40k hôm thứ 3.',
        'Hôm qua đi ăn với bạn hết 10 sịch',
        'Đầu tuần thứ 3 đi ăn với bạn hết 10 sịch',
    ]
    values = [
        'Thứ bảy',
        'Thứ ba',
        'Undefine',
        'Thứ ba',
    ]

    # Add few-shot examples to the history
    messages = [
        {
            "role": "system",
            "content": MENTIONED_DATE_EXTRACT_SYSTEM_PROMPT,
        },
    ]
    for i in range(len(sentences)):
        messages.extend([
            {
                "role": "user",
                "content": sentences[i],
            },
            {
                "role": "assistant",
                "content": values[i],
            },
        ])
    messages.append({
        "role": "user",
        "content": sentence,
    })

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


async def process_rows_async(df, n_samples):
    """Process rows asynchronously in batches"""
    tasks = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        try:
            user = row['user'].split('\n')[0]
            json_dict = json.loads(filter_json_markdown(row['json']))
            tasks.append((idx, user, json_dict))

            # Process in batches of n_samples
            if len(tasks) >= n_samples:
                await process_batch(tasks, df)
                tasks = []

        except Exception as e:
            print(f"Error at index {idx}: {e}")

    # Process remaining tasks
    if tasks:
        await process_batch(tasks, df)


async def process_batch(tasks, df):
    """Process a batch of tasks"""
    results = await asyncio.gather(
        *[predict_time_async(task[1]) for task in tasks],
        return_exceptions=True
    )
    for (idx, _, json_dict), result in zip(tasks, results):
        try:
            mentioned_date_new = result if result != 'Undefine' else None
            df.at[idx, 'mentioned_date'] = json_dict['mentioned_date']
            df.at[idx, 'predict_mentioned_date'] = mentioned_date_new

            json_dict['mentioned_date'] = mentioned_date_new
            json_str = json.dumps(json_dict, indent=4, ensure_ascii=False)
            df.at[idx, 'new_json'] = f"```json\n{json_str}\n```"
        except Exception as e:
            print(f"Error processing batch at index {idx}: {e}")
            


async def main():
    path = 'data/data_time_cover_v2/function_calling_v5-no-weekend.csv'
    df = pd.read_csv(path)

    n_samples = 20  # Number of samples to process in parallel
    await process_rows_async(df, n_samples)

    df.to_csv('data/data_time_cover_v2/function_calling_v5_weekend-fix-v4.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    asyncio.run(main())

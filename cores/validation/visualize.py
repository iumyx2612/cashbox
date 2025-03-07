import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .utils import get_noted_day, get_mentioned_day


VALUE_KEYWORDS = [
    "k", "cành", "nghìn", "ngàn",
    "chục", "sịch", "xị", "sọi",
    "trăm", "lít", "loét", "lốp", "lip", "líp", "list",
    "triệu", 'm', "mê", "củ", "chai", "trai",
    "tỷ", "tỉ", "tỏi"
]


DAY_MAPPING_MATRIX = {
    "hai": 0,
    "ba": 1,
    "tư": 2,
    "năm": 3,
    "sáu": 4,
    "bảy": 5,
    "chủ nhật": 6,
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5
}


def day_interaction_matrix(
    input_file: str,
    output_img_path: str
) -> None:
    df = pd.read_csv(input_file).dropna()
    matrix = np.zeros((7, 7))

    for i in range(len(df)):
        sample = df.iloc[i]["user"]
        mentioned_day = get_mentioned_day(sample.split("\n")[0])
        if mentioned_day:
            noted_day = get_noted_day(sample)
            if noted_day.lower() != "chủ nhật":
                noted_day = noted_day.split()[-1]

            matrix[DAY_MAPPING_MATRIX[mentioned_day.lower()], DAY_MAPPING_MATRIX[noted_day.lower()]] += 1

    fig, ax = plt.subplots()
    cax = ax.imshow(matrix)
    ax.axis('off')
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix[i, j]}", ha='center', va='center', color='white')

    plt.savefig(output_img_path)


def money_keyword_counter(
        input_file: str,
        output_file: str
) -> None:
    df = pd.read_csv(input_file).dropna()
    kw_counter = {kw: 0 for kw in VALUE_KEYWORDS}

    for i in range(len(df)):
        sample = df.iloc[i]["user"]
        for kw in VALUE_KEYWORDS:
            if kw in sample:
                kw_counter[kw] += 1

    values = list(kw_counter.values())
    plt.figure(figsize=(20, 5))
    plt.bar(VALUE_KEYWORDS, values)
    plt.title("Money kw")

    plt.savefig(output_file)
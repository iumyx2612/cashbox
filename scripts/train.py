import os

# turn of gpu 0 
# os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3"

from autotrain.params import LLMTrainingParams
from autotrain.project import AutoTrainProject


params = LLMTrainingParams(
    model="qwen-baseline-money-v5",
    data_path="dataset",
    chat_template="tokenizer",
    model_max_length=1800,
    text_column="text",
    train_split="train",
    trainer="sft",
    epochs=3,
    batch_size=2,
    lr=1e-5,
    mixed_precision="bf16",
    peft=True,
    quantization='int8',
    target_modules="all-linear",
    padding="right",
    optimizer="paged_adamw_8bit",
    scheduler="cosine",
    gradient_accumulation=8,
    merge_adapter=True,
    project_name="qwen-baseline-money-v6-0",
    log="tensorboard",
    push_to_hub=True,
    username='anhalu', 
    token=os.getenv('hf_token'),
)


backend = "local"
project = AutoTrainProject(params=params, backend=backend, process=True)
project.create()
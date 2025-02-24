import os

# let's use gpu 1, 2, 3
os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3"


from autotrain.params import LLMTrainingParams
from autotrain.project import AutoTrainProject


params = LLMTrainingParams(
    model="Qwen/Qwen2.5-7B-Instruct",
    data_path="data",
    chat_template="tokenizer",
    model_max_length=1800,
    text_column="text",
    train_split="train",
    trainer="sft",
    epochs=10,
    batch_size=1,
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
    project_name="qwen-v1",
    log="tensorboard",
    push_to_hub=False,
)


backend = "local"
project = AutoTrainProject(params=params, backend=backend, process=True)
project.create()
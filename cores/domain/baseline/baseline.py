import json
from functools import cached_property
from openai import OpenAI
from openai import AsyncOpenAI
from pydantic import BaseModel
import asyncio

from utils import get_logger
from utils import filter_json_markdown
from schema import Node
from schema import CashFlowInformation
from prompts import BASELINE_SYSTEM_STR
from utils.BaselineSettings import BaselineSettings
from output_parser.vi_pydantic import ViPydanticOutputParser
from utils.utils import time_decorator


logger = get_logger(__name__)

class BaselinePredictor(BaseModel):
    baseline_settings: BaselineSettings
    
    @cached_property
    def client(self): 
        return AsyncOpenAI(
            base_url=f"{self.baseline_settings.base_url}:{self.baseline_settings.port}/v1",
            api_key=self.baseline_settings.api_key
        )
        
    @cached_property
    def system_prompt(self):
        output_parser = ViPydanticOutputParser(CashFlowInformation)
        return f"{BASELINE_SYSTEM_STR}\n{output_parser.format_string}"
    

    async def apredict(self, user_prompt) -> CashFlowInformation:
        """
        Predict the baseline task based on the user prompt.
        """
        completion = await self.client.chat.completions.create(
            model=self.baseline_settings.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        content = completion.choices[0].message.content
        content = filter_json_markdown(content)
        try: 
            content = json.loads(content)
            cash_flow_info = CashFlowInformation(**content)
        except json.JSONDecodeError:
            await logger.aerror(f"Failed to decode JSON: {content}")
            raise ValueError("Invalid JSON response from the model.")
        return cash_flow_info

    def run(self, node: Node) -> Node:
        """
        Run the prediction on the given node.
        """
        return asyncio.run(self.arun(node))
    
    @time_decorator(predictor_name="baseline-predictor")
    async def arun(self, node: Node) -> Node: 
        """
        Run the prediction on the given node.
        """
        user_prompt = node.user_prompt
        await logger.ainfo(f"User Prompt: {user_prompt}\n")
        
        try:
            baseline = await self.apredict(user_prompt)
            node.baseline = baseline
            await logger.ainfo(f"Baseline Prediction: {baseline}\n")
        except Exception as e:
            await logger.aerror(f"Error during prediction: {e}")
            raise e
        
        return node

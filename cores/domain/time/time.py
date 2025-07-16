import json
from functools import cached_property
from openai import OpenAI
from openai import AsyncOpenAI
from pydantic import BaseModel
import asyncio

from utils import get_logger
from utils import filter_json_markdown
from schema import Node
from schema.time_tool import calculate_time
from prompts import FUNCTION_CALLING_TIME_SYSTEM_PROMPT
from utils.TimeSettings import TimeSettings
from utils.utils import time_decorator

logger = get_logger(__name__)

class TimePredictor(BaseModel):
    time_settings: TimeSettings
    
    @cached_property
    def client(self): 
        return AsyncOpenAI(
            base_url=f"{self.time_settings.base_url}:{self.time_settings.port}/v1",
            api_key=self.time_settings.api_key
        )
        
    @cached_property
    def system_prompt(self):
        return FUNCTION_CALLING_TIME_SYSTEM_PROMPT

    async def apredict(self, user_prompt) -> dict:
        """
        Predict the time-related task based on the user prompt.
        """
        completion = await self.client.chat.completions.create(
            model=self.time_settings.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0, 
            extra_body={ 
                "chat_template_kwargs": {"enable_thinking": False},
            },
        )
        content = completion.choices[0].message.content
        content = filter_json_markdown(content)
        try: 
            time_dict = json.loads(content)
            time_value = calculate_time(**time_dict)
        except json.JSONDecodeError:
            await logger.aerror(f"Failed to decode JSON: {content}")
            raise ValueError("Invalid JSON response from the model.")
        return {"time_value": time_value, "time_dict": time_dict}

    def run(self, node: Node) -> Node:
        """
        Run the prediction on the given node.
        """
        return asyncio.run(self.arun(node))
    
    @time_decorator("time_predictor")
    async def arun(self, node: Node) -> Node: 
        """
        Run the prediction on the given node.
        """
        user_prompt = node.user_prompt
        await logger.ainfo(f"User Prompt: {user_prompt}\n")
        
        try:
            time_result = await self.apredict(user_prompt)
            node.time_function_calling = time_result['time_dict']
            node.time = time_result['time_value']
            node.update_baseline_with_time()
            await logger.ainfo(f"Time Prediction: {time_result}\n")
        except Exception as e:
            await logger.aerror(f"Error during prediction: {e}")
            raise e
        
        return node
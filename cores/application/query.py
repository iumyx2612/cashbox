from pydantic import BaseModel
import asyncio

from schema import Node
from schema import CashFlowInformation
from domain.time.time import TimePredictor
from domain.baseline.baseline import BaselinePredictor
from utils import get_logger, get_settings
from utils.setting import Settings
from functools import cached_property
from typing import Literal 
logger = get_logger(__name__)

class QueryInput(BaseModel): 
    query: str
    day: Literal["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ Nhật"]
    function_calling_time: bool = False


class QueryOutput(BaseModel): 
    node: Node
    cashflow_information: CashFlowInformation


class QueryService(BaseModel):
    settings: Settings = get_settings()
    
    @cached_property
    def baseline_predictor(self) -> BaselinePredictor:
        """
        Initialize the BaselinePredictor.
        """
        return BaselinePredictor(baseline_settings=self.settings.baseline)
    
    @cached_property
    def time_predictor(self) -> TimePredictor:
        """
        Initialize the TimePredictor.
        """
        return TimePredictor(time_settings=self.settings.time)
    
    def process(self, inputs: QueryInput) -> QueryOutput:
        return asyncio.run(self.aprocess(inputs))
    
    async def aprocess(self, inputs: QueryInput) -> QueryOutput:
        """
        Process the query using TimePredictor and BaselinePredictor.
        """
        await logger.ainfo("Starting query processing...")
        node = Node(
            query=inputs.query,
            day=inputs.day
        )

        logger.info(f"Initial node created: {node}")

        try:
            logger.info("Running BaselinePredictor...")
            node = await self.baseline_predictor.arun(node)
            logger.info(f"Baseline prediction completed: {node.baseline}")
        except Exception as e:
            logger.error(f"Error in BaselinePredictor: {e}")
            raise e

        if inputs.function_calling_time:
            try: 
                logger.info("Running TimePredictor...")
                node = await self.time_predictor.arun(node)
                logger.info(f"Time prediction completed: {node.time}")
            except Exception as e:
                logger.error(f"Error in TimePredictor: {e}")
                raise e
        logger.info("Query processing completed.")
        return QueryOutput(
            node=node,
            cashflow_information=node.baseline
        )
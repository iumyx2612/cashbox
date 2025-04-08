from pydantic import BaseModel, Field

from prompts import (
    BASELINE_USER_STR
)

from .cashbox import CashFlowInformation
from .time import TimeInformation
from functools import cached_property

class Node(BaseModel): 
    query: str | None = Field(default=None, description="The query string") 

    day: str | None = Field(default=None, description="The day of the week")
    
    # create user_prompt user BASELINE_USER_STR
    # need cache for user_prompt, not need to call every time
    @cached_property
    def user_prompt(self) -> str:
        """
        Generate the user prompt for the model based on the query and day.
        """
        return BASELINE_USER_STR.format(sentence=self.query, day=self.day)
    
    baseline: CashFlowInformation | None = Field(
        default=None,
        description="The baseline information extracted from the query"
    )
    # create baseline_predictor function
    
    time: TimeInformation | None = Field(
        default=None,
        description="The time information extracted from the query"
    )
    
    time_function_calling: str | None = Field(
        default=None,
        description="Parameter for time function calling"
    )
    
    # update time into baseline if time not None 
    def update_baseline_with_time(self):
        """
        Update the baseline with time information if time is not None.
        """
        if self.time and self.baseline:
            self.baseline.when = self.time

    running_time: dict = Field(
        default={},
        description="The time taken to run the prediction"
    )
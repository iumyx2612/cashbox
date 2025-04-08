from application.query import QueryService
from application.query import QueryInput
from application.query import QueryOutput
from utils import get_settings 
from schema import Node

settings = get_settings()


sentence = "Đi chơi ở hội an hết 1 củ 2" 
day = "Thứ ba"

query_input = QueryInput(
    query=sentence,
    day=day,
    function_calling_time=True
)
query_service = QueryService(settings=settings)
result = query_service.process(query_input)
print(result)
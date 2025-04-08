import os
from fastapi import APIRouter
from fastapi import FastAPI, Header, HTTPException, Depends, status
from application import QueryService, QueryInput, QueryOutput
from utils import get_settings

# Initialize the router
query_router = APIRouter(prefix='/v1')

# Initialize QueryService
settings = get_settings()
query_service = QueryService(settings=settings)
EXPECTED_TOKEN=os.getenv("SECURITY_TOKEN")

def verify_token(x_token: str = Header(...)):
    """Simple token authentication dependency."""
    if x_token != EXPECTED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Token"
        )
    return x_token

@query_router.post("/query", response_model=QueryOutput, dependencies=[Depends(verify_token)])
async def query_endpoint(query_input: QueryInput):
    """
    Endpoint to process a query using QueryService.
    """
    try:
        result = await query_service.aprocess(query_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@query_router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
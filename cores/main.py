from api.router import query_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from utils import setup_logging


setup_logging(log_level='INFO')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(
    query_router,
)


@app.get('/')
async def index():
    """Redirect to docs page

    Returns:
        RedirectResponse: docs page
    """
    return RedirectResponse(url='/docs')
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM
from src.database.logging import query_logging
from fastapi.responses import RedirectResponse
from src.routes.api import api_router

DEBUG_SQL_QUERIES = True

app = FastAPI(
    title="Notes API",
    description="Backend of the vue notes application",
    version="alpha 0.1"
)

# add cores headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# register database ORM tortoise
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False  # schemas are generated with aerich/migrations
)

if DEBUG_SQL_QUERIES:
    query_logging()


@app.get("/", include_in_schema=False)
def root_page():
    """ make root path show the API swagger docs """
    return RedirectResponse("/docs")

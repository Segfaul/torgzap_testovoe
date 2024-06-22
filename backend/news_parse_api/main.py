import time
import asyncio

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from backend.news_parse_api.router import news_router

tags_metadata = [
    {
        "name": "News Parse",
        "description": "NewsParse endpoint",
    },
]

app = FastAPI(
    title="NewsParse Public API",
    summary="Chilled api service for parsing news 🐍",
    version='0.0.1',
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_url='/api/openapi.json',
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None
)

app.include_router(news_router, prefix="/api")


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    """
    TIMEOUT Middleware, throws an error if request exceeds 5s
    """
    start_time = time.time()
    try:
        return await asyncio.wait_for(call_next(request), timeout=5)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {
                'detail': 'Request processing time excedeed limit',
                'processing_time': process_time
            },
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )


@app.get("/api/swagger", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json", title="NewsParseAPI",
    )


@app.get("/api/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/api/openapi.json", title="NewsParseAPI",
    )

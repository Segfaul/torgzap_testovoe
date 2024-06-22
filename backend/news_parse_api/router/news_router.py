from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException, status, Request, BackgroundTasks
from pydantic import ValidationError

from backend.news_parse_api.schema import NewsResponse
from backend.news_parse_api.service.parse import run_requests_parser, run_selenium_parser

router = APIRouter(
    prefix="/v1/news",
    tags=['NewsParse']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[NewsResponse], response_model_exclude_unset=True
)
async def read_all_news(
    request: Request,
    file_name: str
):
    try:
        data = pd.read_csv(file_name)
        news_list = data.to_dict(orient='records')
        return [NewsResponse(**news).model_dump(exclude_unset=True) for news in news_list]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=500, detail="CSV file is empty")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {e}")


@router.post(
    '/requests', status_code=status.HTTP_201_CREATED
)
async def create_request_news(
    request: Request, background_tasks: BackgroundTasks
):
    background_tasks.add_task(run_requests_parser)
    return {"status_code": 201, "message": "success"}

@router.post(
    '/selenium', status_code=status.HTTP_201_CREATED
)
async def create_selenium_news(
    request: Request, background_tasks: BackgroundTasks
):
    background_tasks.add_task(run_selenium_parser)
    return {"status_code": 201, "message": "success"}

from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.news_parse_api.util import _AllOptionalMeta


class NewsSchema(BaseModel):
    """
    Pydantic schema for News table data.

    Attributes:
    -----------
    - category: news's category.
    - title: news's title.
    - link: news's link.
    - description: news' description (optional).
    """
    category: str
    title: str
    link: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PartialMemeSchema(NewsSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for News table data (PATCH). 
    """


class IndependentNewsSchema(NewsSchema):
    """
    Pydantic schema for News table data (subqueries).

    Attributes:
    -----------
    - category: news's category.
    - title: news's title.
    - link: news's link.
    - description: news' description (optional).
    """


class NewsResponse(IndependentNewsSchema):
    """
    Pydantic schema for Meme table data.

    Attributes:
    -----------
    - category: news's category.
    - title: news's title.
    - link: news's link.
    - description: news' description (optional).
    """

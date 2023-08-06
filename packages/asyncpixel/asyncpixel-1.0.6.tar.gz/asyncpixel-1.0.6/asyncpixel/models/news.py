"""News related objects."""
from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    """News Item.

    Args:
        material (str): Material of article.
        data (Optional[int]): Data.
    """

    material: str
    data: Optional[int]


class News(BaseModel):
    """News object.

    Args:
        item (Item): News item.
        link (str): Link to article.
        text (text): Text of news.
        title (str): Title of news article.
    """

    item: Item
    link: str
    text: str
    title: str

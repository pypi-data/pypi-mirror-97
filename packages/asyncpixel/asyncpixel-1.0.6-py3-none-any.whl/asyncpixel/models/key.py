"""Main class for key data."""
import uuid

from pydantic import BaseModel


class Key(BaseModel):
    """Main class for key data.

    Args:
        key (uuid.UUID): key text.
        owner (uuid.UUID): uuid of owner.
        limit (int): Limit of toal queries.
        queries_in_past_min (int): Queries in the past minute.
        total_queries (int): Total queries using the key.
    """

    key: uuid.UUID
    owner: uuid.UUID
    limit: int
    queries_in_past_min: int
    total_queries: int

from pydantic import BaseModel


class Q(BaseModel):
    limit: int = None
    start_after_id: str = None

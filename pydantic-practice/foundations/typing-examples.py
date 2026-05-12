from pydantic import BaseModel
from typing import List, Dict, Optional


class Cart(BaseModel):
    user_id: int
    items: List[str]
    total_price: float
    quantities: Dict[str, int]


class Blog(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

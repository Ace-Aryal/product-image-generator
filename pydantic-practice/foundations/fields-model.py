from pydantic import Basemodel, Field
from typing import Optional


class Employe(Basemodel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee name",
        examples=["Ace Aryal"],
    )
    department: Optional[str] = "General"
    salart: float = Field(..., ge=10000)

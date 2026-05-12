from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address


class Comment(BaseModel):
    id: int
    content: str
    # forward referencing own model
    replies: Optional[List["Comment"]] = []


# this is necessary for forward referencing models
Comment.model_rebuild()

address = Address(city="Kathmandu", street="Lazimpat", postal_code="44600")
user = User(id=1, name="Ace Aryal", address=address)
comment = Comment(id=1, content="Hello", replies=[Comment(id=2, content="Hi there")])

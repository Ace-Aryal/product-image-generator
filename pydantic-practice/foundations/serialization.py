from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    created_at: datetime
    address: Address
    tags: List[str] = []
    # custom json encoder for datetime fields, so that when we serialize the model to json, the datetime fields will be formatted as strings
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}
    )


# create a user instance
user = User(
    id=1,
    name="Ace Aryal",
    email="ace@example.com",
    created_at=datetime.now(),
    address=Address(street="123 Main St", city="Kathmandu", zip_code="44600"),
    tags=["admin", "user"],
)

# using model_dump to serialize the user instance to a dictionary
# not json but a python dict, which can be easily converted to json using json.dumps() if needed
user_dict = user.model_dump()
print(user_dict, "user_dict")
json_user = user.model_dump_json()
print(json_user, "json_user")

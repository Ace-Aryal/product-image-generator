from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    is_active: bool


user_data = {"id": 1, "name": "John Doe", "is_active": "True"}
# note: pydantic also does type coercion, so if we pass a string for the id, it will convert it to an int
user = User(**user_data)
print(user, "user")

from pydantic import BaseModel, field_validator, model_validator, computed_field, Field


class User(BaseModel):
    username: str

    # note: field validator runs at the first evne before str validation
    @field_validator("username")
    def username_validator(self, value):
        if len(value) < 4:
            raise ValueError("username must be at least 4 characters")
        return value


class SignupData(BaseModel):
    password: str
    confirm_password: str

    # note: we can control after or before here
    @model_validator(mode="after")
    def password_match(self, values):
        if not (values.password == values.confirm_password):
            raise ValueError("Passowrd do not match")
        return values


class Product(BaseModel):
    price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity


class Booking(BaseModel):
    user_id: int
    room_id: int
    nights: int = Field(..., ge=1)
    rate_per_night: float

    @field_validator("nights")
    def nights_validator(self, value):
        if value < 1:
            raise ValueError("Value needs to be positive integer")

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.rate_per_night * self.nights

from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str


class Settings(BaseModel):
    app_name: str = "My FastAPI App"
    admin_email: EmailStr = "admin@gmail.com"


def get_settings() -> Settings:
    return Settings()


@app.get("/settings")
# instead of creating dependencies inside the function, they are supplied from outside
def get_settings_endpoint(settings: Settings = Depends(get_settings)):
    return settings


@app.post("/signup")
def signup(user: UserSignUp):
    return {"message": f"User {user.username} signed up successfully!"}

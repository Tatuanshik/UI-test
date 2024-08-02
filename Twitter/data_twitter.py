from pydantic import BaseModel, EmailStr


class TwitterAccount(BaseModel):
    login: str
    password: str
    new_password: str
    email: str

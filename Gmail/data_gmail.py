from pydantic import BaseModel, EmailStr


class GmailAccount(BaseModel):
    email: str
    password: str
    new_password: str
    first_name: str
    last_name: str
    backup_email: str




from pydantic import BaseModel


class Register(BaseModel):
    phone: str
    password: str
    username: str | None = None


class Login(BaseModel):
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
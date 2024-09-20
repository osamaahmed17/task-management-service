from pydantic import BaseModel

class UserCreateInput(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateInput(BaseModel):
    username: str
    email: str
    password: str
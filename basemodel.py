from pydantic import BaseModel, ConfigDict
from typing import Optional

class User(BaseModel):
    name: str
    age: int
    email: str
    admin : Optional[bool] = False

class UserWithPassword(User):
    password: str

class UserResponse(BaseModel):
    message: str
    user: User

class UserCreate(BaseModel):
    name: str
    email: str
    password: str  # Including password for user creation

    class Config:
        # This tells Pydantic to read data as dictionaries
        model_config = ConfigDict(from_attributes=True)
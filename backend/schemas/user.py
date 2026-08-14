from pydantic import BaseModel,EmailStr,Field,field_validator,ConfigDict
import re
from utils.validators import validate_password
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(
        min_length=8,
        max_length=30
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128
    )
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
            "Username can only contain letters, numbers, and underscores."
            )
        return value
    
    @field_validator("password")
    @classmethod
    def password_validation(cls,value:str) -> str:
        return validate_password(value)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    
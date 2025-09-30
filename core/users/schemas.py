from pydantic import BaseModel, Field, field_validator
from typing import Optional


class UserLoginSchema(BaseModel):
    username : str = Field(..., max_length=250,
    description="The username of the user")
    password : str = Field(..., min_length=1, max_length=72, 
    description="The password of the user (max 72 characters)")


class UserRegisterSchema(BaseModel):
    username : str = Field(..., max_length=250,
    description="The username of the user")
    password : str = Field(..., min_length=8, max_length=72, 
    description="The password of the user (8-72 characters)")
    password_confirm : str = Field(..., min_length=8, max_length=72, 
    description="The password confirmation of the user (8-72 characters)")

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("Passwords do not match")
        return password_confirm

class UserRefreshTokenSchema(BaseModel):
    token : str = Field(..., description="The refresh token of the user")
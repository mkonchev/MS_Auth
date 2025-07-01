from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if v.islower():
            raise ValueError("Password must contain one uppercase sym")
        if not set('!@#$%&*').intersection(v):
            raise ValueError(
                "Password must contain at least one symbol like(! @ # $ % & *)"
            )
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

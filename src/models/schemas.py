from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime, timezone

# >>>>> AUTH SCHEMAS <<<<<

# Request: What the user sends
class LoginPayload(BaseModel):
    username: str
    password: str

# Response: What the user receives
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# JWT Claims: What is stored in the token
class UserClaims(BaseModel):
    sub: str
    role: str
    permissions: List[str]

# >>>>> NUMBERS SCHEMAS <<<<<

# Request: What the user sends
class NumberCreate(BaseModel):
    value: int
    
    @field_validator('value')
    def validate_positive_value(cls, value):
        if value <= 0:
            raise ValueError('Value must be greater than 0')
        return value

# Database: What gets stored
class NumberRecord(BaseModel):
    username: str
    value: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Response item: What's shown in GET /numbers (per the requirements)
class NumberDisplay(BaseModel):
    value: int
    created_at: datetime

# Response: Full GET /numbers response
class NumberResponse(BaseModel):
    username: str
    numbers: List[NumberDisplay] = Field(default_factory=list)

# Request: For updating a number
class NumberUpdate(BaseModel):
    value: int
    
    @field_validator('value')
    def validate_positive_value(cls, value):
        if value <= 0:
            raise ValueError('Value must be greater than 0')
        return value

# >>>>> STATISTICS SCHEMAS <<<<<

# Response: Statistics for user's numbers
class NumberStatistics(BaseModel):
    count: int
    sum: int
    average_value: float
    min_value: int | None = None
    max_value: int | None = None

# >>>>> MIDDLEWARE / UTIL SCHEMAS <<<<<

# RFC 7807 - Problem Details for HTTP APIs
class ProblemDetails(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
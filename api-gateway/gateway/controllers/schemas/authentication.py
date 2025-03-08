from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LoginSerializer(BaseModel):
    username: str = Field(..., example="john@yopmail.com")
    password: str = Field(..., example="john@123")

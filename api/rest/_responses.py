from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    username: str
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    token: str

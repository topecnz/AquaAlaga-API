from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    username: str
    password: str


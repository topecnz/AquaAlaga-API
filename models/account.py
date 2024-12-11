from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    username: str
    password: str
    
class Signup(BaseModel):
    username: str
    password: str
    email: str
    
class Verify(BaseModel):
    id: str
    verification_code: int

class Reset(BaseModel):
    id: str
    reset_code: int
    
class ResetPassword(BaseModel):
    id: str
    password: str
    
class ChangePassword(BaseModel):
    id: str
    current_password: str
    password: str
    
class ChangeEmail(BaseModel):
    id: str
    email: str
    
class UpdateAccount(BaseModel):
    id: str
    password: str
    security_question: str
    security_answer: str

class SecurityAnswer(BaseModel):
    id: str    
    security_answer: str
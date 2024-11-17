from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    username: str
    password: str
    
class FirstSetup(BaseModel):
    id: str
    password: str
    security_question: str
    security_answer: str
    
class ResetPassword(BaseModel):
    id: str
    password: str
    
class UpdateAccount(BaseModel):
    id: str
    password: str
    security_question: str
    security_answer: str

class SecurityAnswer(BaseModel):
    id: str    
    security_answer: str
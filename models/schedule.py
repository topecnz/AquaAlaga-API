from pydantic import BaseModel

class Schedule(BaseModel):
    name: str
    time: str
    repeat: str
    timer: int
    is_enable: bool

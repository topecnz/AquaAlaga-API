from pydantic import BaseModel

class Report(BaseModel):
    sensor: str
    data: str

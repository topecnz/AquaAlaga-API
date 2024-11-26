from pydantic import BaseModel

class Report(BaseModel):
    id: str
    temperature: float
    feed: int
    ph_level: float

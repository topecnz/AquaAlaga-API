from pydantic import BaseModel

class Report(BaseModel):
    sensor: str
    data: str
    device_id: str

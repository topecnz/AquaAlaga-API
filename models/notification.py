from pydantic import BaseModel

class Notification(BaseModel):
    message: str
    device_id: str

from pydantic import BaseModel

class Device(BaseModel):
    name: str
    type: str
    mac_address: str
    ip_address: str

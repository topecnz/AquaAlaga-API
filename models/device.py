from pydantic import BaseModel

class Device(BaseModel):
    name: str
    type: str
    mac_address: str
    ip_address: str
    fish_breed: str
    temperature: int
    ph_level: int
    account_id: str

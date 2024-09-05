from pydantic import BaseModel

class Device(BaseModel):
    name: str
    wifi_ssid: str
    wifi_mac_address: str
    password: str

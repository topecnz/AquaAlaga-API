from pydantic import BaseModel

class SensorData(BaseModel):
    sensor: str
    data: str
    
connected_clients = []
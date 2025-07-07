from pydantic import BaseModel
from typing import Optional

class BaseEmergencyContact(BaseModel):
    name: str
    address: str
    phone: str

class CreateEmergencyContact(BaseEmergencyContact):
    pass

class UpdateEmergencyContact(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class ReadEmergencyContact(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True
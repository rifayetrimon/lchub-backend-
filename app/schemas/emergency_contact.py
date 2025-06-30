from pydantic import BaseModel


class BaseEmergencyContact(BaseModel):
    name: str
    address: str
    phone: str


class CreateEmergencyContact(BaseEmergencyContact):
    pass

class UpdateEmergencyContact(BaseEmergencyContact):
    pass

class DeleteEmergencyContact(BaseEmergencyContact):
    pass

class ReadEmergencyContact(BaseEmergencyContact):
    id: int
    pass
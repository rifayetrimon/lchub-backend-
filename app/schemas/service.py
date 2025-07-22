from typing import List
from pydantic import BaseModel


class BaseService(BaseModel):
    name: str
    address: str
    phone: str


class CreateService(BaseService):
    service_category_id: int
    pass

class UpdateService(BaseService):
    service_category_id: int
    pass

class DeleteService(BaseService):
    pass

class ServiceRead(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    service_category_id: int

    class Config:
        from_attributes = True

class ServiceResponse(BaseModel):
    status: str
    message: str
    name: str
    address: str
    phone: str


class ServiceListResponse(BaseModel):
    items: List[ServiceRead]
    total: int


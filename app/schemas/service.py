from pydantic import BaseModel


class BaseService(BaseModel):
    name: str
    address: str
    phone: str


class CreateService(BaseService):
    service_category_id: int
    pass

class UpdateService(BaseService):
    pass

class DeleteService(BaseService):
    pass

class ReadService(BaseService):
    id: int
    pass

class ServiceResponse(BaseModel):
    status: str
    message: str
    name: str
    address: str
    phone: str
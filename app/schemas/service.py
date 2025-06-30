from pydantic import BaseModel


class BaseService(BaseModel):
    name: str
    address: str
    phone: str


class CreateService(BaseService):
    pass

class UpdateService(BaseService):
    pass

class DeleteService(BaseService):
    pass

class ReadService(BaseService):
    id: int
    pass

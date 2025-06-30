from pydantic import BaseModel


class BaseServiceCategory(BaseModel):
    name: str

class CreateServiceCategory(BaseServiceCategory):
    pass

class UpdateServiceCategory(BaseServiceCategory):
    pass

class DeleteServiceCategory(BaseServiceCategory):
    pass

class ServiceCategory(BaseModel):
    name: str

class ReadServiceCategory(BaseServiceCategory):
    pass

from pydantic import BaseModel

from app.schemas.job import BaseJob


class BaseBusinessCategories(BaseModel):
    name: str

class CreateBusinessCategories(BaseBusinessCategories):
    pass

class UpdateBusinessCategories(BaseBusinessCategories):
    pass

class DeleteBusinessCategories(BaseBusinessCategories):
    pass

class ReadBusinessCategories(BaseBusinessCategories):
    id: int
    pass
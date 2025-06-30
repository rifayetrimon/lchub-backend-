from pydantic import BaseModel


class BaseJobCategory(BaseModel):
    name: str


class CreateJobCategory(BaseJobCategory):
    pass


class UpdateJobCategory(BaseJobCategory):
    pass


class DeleteJobCategory(BaseJobCategory):
    pass


class ReadJobCategory(BaseJobCategory):
    id: int
    pass
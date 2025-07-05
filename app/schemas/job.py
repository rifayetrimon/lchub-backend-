import enum
from typing import Optional

from pydantic import BaseModel


class TypeOfJob(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    freelance = "freelance"


class BaseJob(BaseModel):
    job_type: TypeOfJob
    title: str
    location: str
    salary: Optional[float]
    application_email: str
    application_url: str
    description: str
    requirements: str


class CreateJob(BaseJob):
    business_id: int
    pass

    class Config:
        from_attributes = True

class UpdateJob(BaseJob):
    pass

class DeleteJob(BaseJob):
    pass

class ReadJob(BaseJob):
    id: int
    pass

    class Config:
        from_attributes = True


class ServiceResponse(BaseModel):
    status: str
    message: str
    job_type: TypeOfJob
    title: str
    location: str
    salary: float
    application_email: str
    application_url: str
    description: str
    requirements: str



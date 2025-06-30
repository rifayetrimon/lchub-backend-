import enum
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
    salary: float
    application_email: str
    application_url: str
    description: str
    requirements: str


class CreateJob(BaseJob):
    pass

class UpdateJob(BaseJob):
    pass

class DeleteJob(BaseJob):
    pass

class ReadJob(BaseJob):
    id: int
    pass



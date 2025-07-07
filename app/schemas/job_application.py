import enum
from pydantic import BaseModel


class Status(str, enum.Enum):
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"
    reviewed = "reviewed"


class BaseJobApplication(BaseModel):
    cover_letter: str
    cv_url: str
    status: Status


class CreateJobApplication(BaseJobApplication):
    job_id: int
    pass


class UpdateJobApplication(BaseJobApplication):
    pass


class DeleteJobApplication(BaseJobApplication):
    pass


class ReadJobApplication(BaseJobApplication):
    id: int
    user_id: int
    job_id: int

    class Config:
        from_attributes = True
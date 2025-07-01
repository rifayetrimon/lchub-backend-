import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Status(str, enum.Enum):
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"
    reviewed = "reviewed"

# --- JobApplication Model ---
class JobApplication(Base):
    __tablename__ = "job_application"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    cover_letter = Column(String)
    cv_url = Column(String)
    status = Column(Enum(Status))

    user = relationship("User", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")


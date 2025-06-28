import enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Text


class TypeOfJob(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    freelance = "freelance"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_profile.id"))
    title = Column(String, index=True)
    location = Column(String, index=True)
    job_type = Column(Enum(TypeOfJob), nullable=False)
    category_id = Column(Integer, ForeignKey("job_categories.id"))
    salary = Column(Float, nullable=True)
    application_email = Column(String, index=True)
    application_url = Column(String, index=True)
    description = Column(Text, index=True)
    requirements = Column(Text, index=True)

    business = relationship("BusinessProfile", back_populates="jobs")
    category = relationship("JobCategories", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job")



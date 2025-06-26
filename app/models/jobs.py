import enum

from sqlalchemy.orm import relationship

from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, DateTime, Text
class ServiceCategory(Base):
    __tablename__ = "service_categories"


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
    category_id = Column(Integer, ForeignKey("business_categories.id"))
    salary = Column(Float, nullable=True)
    application_email = Column(String, index=True)
    application_url = Column(String, index=True)
    description = Column(Text, index=True)
    requirements = Column(Text, index=True)

    business = relationship("BusinessProfile", backref="jobs")
    category = relationship("BusinessCategories", backref="jobs")





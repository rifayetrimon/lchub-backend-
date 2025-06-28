from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class JobCategories(Base):
    __tablename__ = "job_categories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    jobs = relationship("Job", back_populates="category")
    business_profiles = relationship("BusinessProfile", back_populates="category")


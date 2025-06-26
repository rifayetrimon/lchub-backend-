from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_profile.id"))
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base_class import Base




class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    services = relationship("Service", back_populates="category")

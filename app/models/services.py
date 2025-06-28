from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    service_category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)  # <-- Add this
    name = Column(String, index=True, nullable=False)
    address = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="services")
    category = relationship("ServiceCategory", back_populates="services")  # <-- Add this
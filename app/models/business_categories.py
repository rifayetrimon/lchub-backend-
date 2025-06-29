from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BusinessCategories(Base):
    __tablename__ = "business_categories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    business = relationship("BusinessProfile", back_populates="category")


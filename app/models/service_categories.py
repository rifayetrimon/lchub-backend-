from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    service_category_name = Column(String, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    address = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
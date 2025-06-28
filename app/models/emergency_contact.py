from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    address = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


class UserType(str, enum.Enum):
    student= "student"
    business= "business"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False)


class BusinessProfile(Base):
    __tablename__ = "business_profile"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    business_name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("business_categories.id"), nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    user = relationship("User", back_populates="business_profile")
    category = relationship("BusinessCategories", back_populates="category")
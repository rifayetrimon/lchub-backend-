from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class UserType(str, enum.Enum):
    student = "student"
    business = "business"

class BusinessType(str, enum.Enum):
    individual = "individual"
    company = "company"

# --- User Model ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False)
    services = relationship("Service", back_populates="user")
    job_applications = relationship("JobApplication", back_populates="user")
    reviews = relationship("Review", back_populates="user")

# --- BusinessProfile Model ---
class BusinessProfile(Base):
    __tablename__ = "business_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    business_type = Column(Enum(BusinessType), nullable=False)
    business_name = Column(String, index=True, nullable=True)
    category_id = Column(Integer, ForeignKey("business_categories.id"), nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    registration_number = Column(String, nullable=True)

    user = relationship("User", back_populates="business_profile")
    category = relationship("BusinessCategory", back_populates="business_profiles")
    jobs = relationship("Job", back_populates="business")
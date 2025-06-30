import enum
from pydantic import BaseModel, EmailStr, Field, root_validator, model_validator
from typing import Optional


# --- Enums ---
class UserType(str, enum.Enum):
    student = "student"
    business = "business"

class BusinessType(str, enum.Enum):
    individual = "individual"
    company = "company"

# --- BusinessProfile Schema ---
class BusinessProfileBase(BaseModel):
    business_type: BusinessType
    business_name: Optional[str] = None
    category_id: int
    address: str
    phone: str
    registration_number: Optional[str] = None

class BusinessProfileCreate(BusinessProfileBase):
    pass

# --- User Schemas ---
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    user_type: UserType

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)
    business_profile: Optional[BusinessProfileCreate] = None

    @model_validator
    def check_business_fields(cls, values):
        user_type = values.get('user_type')
        business_profile = values.get('business_profile')
        if user_type == UserType.business:
            if not business_profile:
                raise ValueError("Business profile is required for business users.")


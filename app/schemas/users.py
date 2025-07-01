# users/schemas.py
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Optional
import enum



class UserType(str, enum.Enum):
    student = "student"
    business = "business"

class BusinessType(str, enum.Enum):
    individual = "individual"
    company = "company"

class BusinessProfileBase(BaseModel):
    business_type: BusinessType
    business_name: Optional[str] = None
    category_id: int
    address: str
    phone: str
    registration_number: Optional[str] = None

class BusinessProfileCreate(BusinessProfileBase):
    pass

class BusinessProfileResponse(BusinessProfileBase):
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    user_type: UserType

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)
    business_profile: Optional[BusinessProfileCreate] = None

    @model_validator(mode="after")
    def check_business_fields(self):
        if self.user_type == UserType.business:
            if not self.business_profile:
                raise ValueError("Business profile is required for business users.")
        else:
            if self.business_profile:
                raise ValueError("Business profile should not be provided for non-business users.")
        return self

class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    user_type: UserType
    business_profile: Optional[BusinessProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    status: str
    messages: str
    data: UserRead

class Token(BaseModel):
    access_token: str
    token_type: str
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User, UserType, BusinessType, BusinessProfile
from app.schemas.users import UserCreate
from app.core.security import verify_password, create_access_token, hash_password
from fastapi import HTTPException, status



class UserService:
    @staticmethod

    async def register_user(new_user: UserCreate, db: AsyncSession):
        result_email = await db.execute(select(User).where(User.email == new_user.email))
        existing_user_email = result_email.scalar_one_or_none()

        if existing_user_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = hash_password(new_user.password)
        new_user_model = User(
            full_name= new_user.full_name,
            email=new_user.email,
            password=hashed_password,
            user_type=new_user.user_type
        )

        db.add(new_user_model)
        await db.flush()

        if new_user.user_type == UserType.business and new_user.business_profile:
            bp = new_user.business_profile

            business_profile = BusinessProfile(
                user_id=new_user_model.id,
                business_type=bp.business_type,
                business_name=bp.business_name,
                category_id=bp.category_id,
                address=bp.address,
                phone=bp.phone,
                registration_number=bp.registration_number
            )
            db.add(business_profile)

        await db.commit()
        await db.refresh(new_user_model)
        return new_user_model

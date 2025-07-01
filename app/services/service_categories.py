from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.users import User
from app.models.service_categories import ServiceCategory
from fastapi import HTTPException, status
from app.schemas.service_categories import CreateServiceCategory
from sqlalchemy import and_



logger = logging.getLogger(__name__)



class ServiceCategoriesService:

    @staticmethod
    async def _verify_user_authorization(user: User):
        if user.user_type not in ["student", "business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user type",
            )


    @staticmethod
    async def create_service_category(service_category_data: CreateServiceCategory, db: AsyncSession, user: User):
        try:
            await ServiceCategoriesService._verify_user_authorization(user)

            existing_category = await db.execute(
                select(ServiceCategory).where(
                    and_(
                        ServiceCategory.name == service_category_data.name,
                    )
                )
            )

            if existing_category.scalar():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category already exists",
                )

            new_service_category = ServiceCategory(
                **service_category_data.model(exclude={"user_id"}),
                user_id = user.id
            )

            try:
                db.add(new_service_category)
                db.commit()
                db.refresh(new_service_category)

            except Exception as e:
                await db.rollback()
                logger.error(f"Failed to create new service_category: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Failed to create new service_category",
                )

            return new_service_category
















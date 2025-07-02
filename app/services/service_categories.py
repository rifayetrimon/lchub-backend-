from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.service_categories import ServiceCategory
from fastapi import HTTPException, status
from app.schemas.service_categories import CreateServiceCategory
from sqlalchemy import and_

logger = logging.getLogger(__name__)

class ServiceCategoriesService:

    @staticmethod
    async def create_service_category(service_category_data: CreateServiceCategory, db: AsyncSession):
        try:
            # Check if the category already exists
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

            # Create a new service category
            new_service_category = ServiceCategory(
                **service_category_data.model_dump()  # Adjust based on your schema
            )

            # Add and commit the new service category
            db.add(new_service_category)
            await db.commit()  # Use await for async commit
            await db.refresh(new_service_category)  # Use await for async refresh

            return new_service_category

        except Exception as e:
            await db.rollback()  # Rollback on error
            logger.error(f"Failed to create new service category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create new service category",
            )
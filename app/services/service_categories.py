from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.service_categories import ServiceCategory
from fastapi import HTTPException, status
from app.schemas.service_categories import CreateServiceCategory, UpdateServiceCategory
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


    @staticmethod
    async def get_service_categories(db: AsyncSession):
        try:
            result = await db.execute(select(ServiceCategory))
            categories = result.scalars().all()
            return categories
        except Exception as e:
            logger.error(f"Failed to get service categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get service categories",
            )


    @staticmethod
    async def get_service_category_by_id(service_category_id: int, db: AsyncSession):
        try:
            result = await db.execute(
                select(ServiceCategory).where(ServiceCategory.id == service_category_id)
            )

            categrory = result.scalar_one_or_none()

            if not categrory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service category not found",
                )

            return categrory

        except Exception as e:
            logger.error(f"Failed to get service categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get service categories",
            )



    @staticmethod
    async def update_service_category(service_category_id: int, service_category_data: UpdateServiceCategory, db: AsyncSession):
        try:
            result = await db.execute(
                select(ServiceCategory).where(ServiceCategory.id == service_category_id)
            )

            category = result.scalar_one_or_none()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service category not found",
                )

            for key, value in service_category_data.model_dump().items():
                setattr(category, key, value)

            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category

        except Exception as e:
            logger.error(f"Failed to update service category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update service category",
            )



    @staticmethod
    async def delete_service_category(service_category_id: int, db: AsyncSession):
        try:
            result = await db.execute(
                select(ServiceCategory).where(ServiceCategory.id == service_category_id)
            )

            category = result.scalar_one_or_none()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service category not found",
                )

            await db.delete(category)
            await db.commit()
            await db.refresh(category)
            return category
        except Exception as e:
            logger.error(f"Failed to delete service category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete service category",
            )

















import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from app.models import BusinessCategory
from app.schemas.service import BaseService
from app.schemas.business_categories import CreateBusinessCategories

logger = logging.getLogger(__name__)



class BusinessCategoriesService(BaseService):

    @staticmethod
    async def Create_business_category(business_category_data: CreateBusinessCategories, db: AsyncSession):
        try:
            existing_category = await db.execute(
                select(BusinessCategory).where(BusinessCategory.name == business_category_data.name)
            )

            if existing_category.scalar():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Business category already exists",
                )

            new_business_category = BusinessCategory(
                **business_category_data.model_dump()
            )

            db.add(new_business_category)
            await db.commit()
            await db.refresh(new_business_category)

            return new_business_category

        except Exception as e:
            logger.error(f"Failed to create business category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create business category",
            )


    @staticmethod
    async def get_all_business_categories(db: AsyncSession):
        try:
            business_categories = await db.execute(
                select(BusinessCategory)
            )
            categories = business_categories.scalars().all()
            return categories
        except Exception as e:
            logger.error(f"Failed to get business categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get business categories",
            )

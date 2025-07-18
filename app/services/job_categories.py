import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_categories import CreateJobCategory, UpdateJobCategory
from app.schemas.service import BaseService
from app.models.job_categories import JobCategory



logger = logging.getLogger(__name__)


class JobCategoriesService(BaseService):

    @staticmethod
    async def create_job_category(job_category_date: CreateJobCategory, db: AsyncSession):
        try:
            existing_category = await db.execute(
                select(JobCategory).where(
                    and_(
                        JobCategory.name == job_category_date.name,
                    )
                )
            )

            if existing_category.scalar():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Job category already exists",
                )

            new_job_category = JobCategory(
                **job_category_date.model_dump()
            )

            db.add(new_job_category)
            await db.commit()
            await db.refresh(new_job_category)

            return new_job_category

        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create job category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job category",
            )


    @staticmethod
    async def get_job_categories(db: AsyncSession, skip: int = 0):
        try:
            fixed_limit = 15  # Always return 15 items
            stmt = select(JobCategory).offset(skip).limit(fixed_limit)
            result = await db.execute(stmt)
            job_categories = result.scalars().all()
            return job_categories

        except Exception as e:
            logger.error(f"Failed to get job categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job categories",
            )

    @staticmethod
    async def get_job_category_by_id(job_category_id: int, db: AsyncSession):
        try:
            job_category = await db.execute(
                select(JobCategory).where(JobCategory.id == job_category_id)
            )

            category = job_category.scalar_one_or_none()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job category not found",
                )
            return category

        except Exception as e:
            logger.error(f"Failed to get job categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job categories",
            )


    @staticmethod
    async def update_job_category(job_category_id: int ,job_category_date: UpdateJobCategory, db: AsyncSession):
        try:
            result = await db.execute(
                select(JobCategory).where(JobCategory.id == job_category_id)
            )

            category = result.scalar_one_or_none()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job category not found",
                )

            for key, value in job_category_date.model_dump().items():
                setattr(category, key, value)


            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category

        except Exception as e:
            logger.error(f"Failed to update job category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update job category",
            )


    @staticmethod
    async def delete_job_category(job_category_id: int, db: AsyncSession):
        try:
            job_category = await db.execute(
                select(JobCategory).where(JobCategory.id == job_category_id)
            )

            category = job_category.scalar_one_or_none()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job category not found",
                )

            await db.delete(category)
            await db.commit()
            await db.refresh(category)
            return category

        except Exception as e:
            logger.error(f"Failed to delete job category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete job category",
            )
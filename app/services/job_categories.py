import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_categories import CreateJobCategory
from app.schemas.service import BaseService
from app.models.job_categories import JobCategory



logger = logging.getLogger(__name__)


class JobCategoriesService(BaseService):

    @staticmethod
    async def create_job_category(job_category_date: CreateJobCategory, db: AsyncSession):
        try:
            exixting_category = await db.execute(
                select(JobCategory).where(
                    and_(
                        JobCategory.name == job_category_date.name,
                    )
                )
            )

            if exixting_category.scalar():
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
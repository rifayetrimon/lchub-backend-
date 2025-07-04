import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.models.jobs import Job, TypeOfJob
from app.schemas.job import CreateJob, ReadJob, UpdateJob, DeleteJob



logger = logging.getLogger(__name__)


class JobService:

    @staticmethod
    async def _verify_user_type_authentication(user: User):
        if user.user_type not in ["business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not able to create job",
            )


    @staticmethod
    async def create_job(user: User, create_job_data: CreateJob, db: AsyncSession):
        try:
            await JobService._verify_user_type_authentication(user)

            new_job = Job(
                **create_job_data.model_dump(),
            )


            db.add(new_job)
            await db.commit()
            await db.refresh(new_job)

            return new_job

        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create job: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job",
            )


import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status
from app.models.users import User, BusinessProfile
from app.models.job_application import JobApplication
from app.schemas.job_application import CreateJobApplication, Status



logger = logging.getLogger(__name__)


class JobApplicationService:

    @staticmethod
    async def _verify_user_authentication(user: User, db: AsyncSession):
        if user.user_type == "student":
            return

        if user.user_type == "business":
            # Fetch business profile separately
            result = await db.execute(
                select(BusinessProfile).where(BusinessProfile.user_id == user.id)
            )
            business_profile = result.scalar_one_or_none()

            if business_profile and business_profile.business_type == "individual":
                return

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    @staticmethod
    async def create_job_application(db: AsyncSession, job_create_data: CreateJobApplication, user: User):
        try:
            await JobApplicationService._verify_user_authentication(user, db)

            # Check if user has already applied for this specific job
            existing = await db.execute(
                select(JobApplication).where(
                    JobApplication.user_id == user.id,
                    JobApplication.job_id == job_create_data.job_id
                )
            )

            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You have already applied for this job",
                )

            # Create new job application
            application_data = job_create_data.model_dump()
            application_data["user_id"] = user.id
            application_data["status"] = Status.submitted

            new_application = JobApplication(**application_data)

            db.add(new_application)
            await db.commit()
            await db.refresh(new_application)

            return new_application

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create job application: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job application",
            )
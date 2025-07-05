import logging
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, BusinessProfile
from app.models.jobs import Job
from app.schemas.job import CreateJob, ServiceResponse, UpdateJob, ReadJob

logger = logging.getLogger(__name__)

class JobService:

    @staticmethod
    async def _verify_user_type_authentication(user: User):
        if user.user_type != "business":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to create a job",
            )

    @staticmethod
    async def create_job(user: User, create_job_data: CreateJob, db: AsyncSession) -> ServiceResponse:
        try:
            await JobService._verify_user_type_authentication(user)

            result = await db.execute(
                select(BusinessProfile).where(BusinessProfile.user_id == user.id)
            )
            business_profile = result.scalars().first()

            if not business_profile:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Business profile not found for the user",
                )

            job_data = create_job_data.model_dump()
            job_data.pop('business_id', None)
            job_data['business_id'] = business_profile.id

            new_job = Job(**job_data)

            db.add(new_job)
            await db.commit()
            await db.refresh(new_job)

            # Return a response matching ServiceResponse schema
            return ServiceResponse(
                status="success",
                message="Job created successfully",
                job_type=new_job.job_type,
                title=new_job.title,
                location=new_job.location,
                salary=new_job.salary,
                application_email=new_job.application_email,
                application_url=new_job.application_url,
                description=new_job.description,
                requirements=new_job.requirements,
            )

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create job: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job",
            )


    @staticmethod
    async def get_all_jobs(db: AsyncSession):
        try:
            job = await db.execute(
                select(Job)
            )

            jobs = job.scalars().all()
            return jobs

        except Exception as e:
            logger.error(f"Failed to get all jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get all jobs",
            )

    @staticmethod
    async def get_job_by_id(job_id: int, db: AsyncSession):
        try:
            job = await db.execute(
                select(Job).where(Job.id == job_id)
            )

            rslt = job.scalar_one_or_none()

            return rslt

        except Exception as e:
            logger.error(f"Failed to get job by id: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job by id",
            )

    @staticmethod
    async def update_job(job_id: int, user: User, job_data_update: UpdateJob, db: AsyncSession):
        await JobService._verify_user_type_authentication(user)

        # Get the job
        job = await JobService.get_job_by_id(job_id, db)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        # Get the business profile for the current user
        result = await db.execute(
            select(BusinessProfile).where(BusinessProfile.user_id == user.id)
        )
        business_profile = result.scalars().first()

        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found for the user",
            )

        # Check if the job belongs to the user's business profile
        if job.business_id != business_profile.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to update this job",
            )

        # Update the job fields
        update_data = job_data_update.model_dump(exclude_unset=True, exclude={"business_id"})
        for key, value in update_data.items():
            setattr(job, key, value)

        try:
            await db.commit()
            await db.refresh(job)

            # Return updated job as ReadJob schema
            return ReadJob.from_orm(job)

        except Exception as e:
            logger.error(f"Failed to update job: {str(e)}", exc_info=True)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update job",
            )



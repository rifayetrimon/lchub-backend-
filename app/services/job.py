import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.models.jobs import Job, TypeOfJob
from app.schemas.job import CreateJob, ReadJob, UpdateJob, DeleteJob



logger = logging.getLogger(__name__)


class JobService:

    @staticmethod
    async def _verify_user_authentication(user: User):
        if user.user_type not in ["business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not able to create job",
            )


    @staticmethod
    async def create_job()
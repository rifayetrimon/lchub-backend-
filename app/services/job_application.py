import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import User
from app.schemas.job_application import BaseJobApplication



logger = logging.getLogger(__name__)



class JobApplicationService(BaseJobApplication):

    @staticmethod
    async def _verify_user_authentication(user: User, db: AsyncSession):
        if not (user.user_type == "student" or (user.user_type == "business" and getattr(user.business_profile, "business_type", None) == "individual")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )












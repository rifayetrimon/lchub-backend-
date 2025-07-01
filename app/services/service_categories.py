from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.users import User
from app.models.service import Service
from fastapi import HTTPException, status
from app.schemas.service import CreateService, ServiceResponse
from sqlalchemy import and_



logger = logging.getLogger(__name__)



class ServiceCategoriesService:

    @staticmethod
    async def _verify_user_authorization(user: User):
        if user.user_type not in ["student", "business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user type",
            )


    # @staticmethod
    # async def create_service_category(user: User, service_data: CreateService, db: AsyncSession):
    #     try:
    #















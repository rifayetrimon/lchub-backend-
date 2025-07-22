from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.users import User
from app.models.service import Service
from fastapi import HTTPException, status
from app.schemas.service import CreateService, ServiceResponse, UpdateService
from sqlalchemy import and_, func



logger = logging.getLogger(__name__)



class TypeServices:

    @staticmethod
    async def _verify_user_authorization(user: User):
        if user.user_type not in ["student", "business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user type",
            )

    @staticmethod
    async def create_service(user: User, service_data: CreateService, db: AsyncSession):
        try:
            await TypeServices._verify_user_authorization(user)

            existing = await db.execute(
                select(Service).where(
                    and_(Service.name == service_data.name, Service.created_by == user.id)
                )
            )

            if existing.scalar():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Service already exists",
                )

            new_service = Service(
                **service_data.model_dump(exclude={"created_by"}),
                created_by=user.id
            )

            db.add(new_service)
            await db.commit()  # Use await for async commit
            await db.refresh(new_service)  # Use await for async refresh

            return ServiceResponse(
                name=new_service.name,
                address=new_service.address,
                phone=new_service.phone
            )


        except Exception as e:
            await db.rollback()  # Rollback on error
            logger.error(f"Service creation failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Service creation failed: {str(e)}",
            )

    # @staticmethod
    # async def get_all_services(db: AsyncSession, skip: int = 0, limit: int = 12):
    #     try:
    #         # Count total services
    #         total_stmt = select(func.count(Service.id))
    #         total_result = await db.execute(total_stmt)
    #         total = total_result.scalar()
    #
    #         # Get paginated services
    #         stmt = select(Service).offset(skip).limit(limit)
    #         result = await db.execute(stmt)
    #         services = result.scalars().all()
    #
    #         return {
    #             "total": total,
    #             "items": services
    #         }
    #     except Exception as e:
    #         logger.error(f"Service retrieval failed: {str(e)}", exc_info=True)
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Service retrieval failed: {str(e)}"
    #         )

    @staticmethod
    async def get_all_services(db: AsyncSession, skip: int = 0):
        try:
            fixed_limit = 12  # Always return 10 items
            stmt = select(Service).offset(skip).limit(fixed_limit)
            result = await db.execute(stmt)
            services = result.scalars().all()
            return services
        except Exception as e:
            logger.error(f"Service retrieval failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Service retrieval failed: {str(e)}",
            )

    @staticmethod
    async def get_service(service_id: int, db: AsyncSession):
        try:
            stmt = select(Service).where(Service.id == service_id)        # B-tree DS
            result = await db.execute(stmt)
            service = result.scalar_one_or_none()

            if service is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Service with ID {service_id} not found"
                )

            return service

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving Service ID {service_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while retrieving the service."
            )


    @staticmethod
    async def update_service(service_id: int, user: User, service_data: UpdateService, db: AsyncSession):
        await TypeServices._verify_user_authorization(user)

        service = await TypeServices.get_service(service_id, db)

        if service.created_by != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this service",
            )

        update_data = service_data.model_dump(exclude_unset=True, exclude={"created_by"})
        for key, value in update_data.items():
            setattr(service, key, value)

        try:
            await db.commit()
            await db.refresh(service)
            return service
        except Exception as e:
            await db.rollback()
            logger.error(f"Service update failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Service update failed: {str(e)}",
            )


    @staticmethod
    async def delete_service(service_id: int, user: User, db: AsyncSession):
        await TypeServices._verify_user_authorization(user)

        # Fetch the service to delete
        service = await TypeServices.get_service(service_id, db)

        # Check if the service belongs to the user (optional)
        if service.created_by != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this service",
            )

        try:
            await db.delete(service)
            await db.commit()
            return {"status": "success", "message": "Service deleted successfully"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Service deletion failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Service deletion failed: {str(e)}",
            )



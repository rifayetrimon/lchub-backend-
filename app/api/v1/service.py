from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.service import CreateService, ServiceResponse
from app.models.users import User
from app.api.deps import get_current_user
from app.services.service import TypeServices

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/create", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
        service: CreateService,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Ensure current_user is a valid User object
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Call the service creation method
    new_service = await TypeServices.create_service(current_user, service, db)

    return new_service
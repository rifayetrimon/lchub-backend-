from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.service import CreateService, ServiceResponse, ServiceRead, UpdateService, ServiceListResponse
from app.models.users import User
from app.api.deps import get_current_user
from app.services.service import TypeServices
from fastapi import Query


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


# @router.get("/", response_model=List[ServiceRead])
# async def read_all_services(skip: int = 0, db: AsyncSession = Depends(get_db)):
#     services = await TypeServices.get_all_services(db, skip=skip)
#     return services


@router.get("/", response_model=ServiceListResponse, status_code=status.HTTP_200_OK)
async def read_all_services(skip: int = 0, limit: int = 12, db: AsyncSession = Depends(get_db)):
    items, total = await TypeServices.get_all_services(db, skip=skip, limit=limit)
    return {"items": items, "total": total}



@router.get(
    "/{id}",
    response_model=ServiceRead,
    summary="Get a service by ID",
    responses={
        404: {"description": "Service not found"},
        500: {"description": "Internal server error"},
    },
)
async def read_service(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    return await TypeServices.get_service(service_id=id, db=db)


@router.put("/{service_id}", response_model=ServiceRead, status_code=status.HTTP_200_OK)
async def update_service(
    service_id: int,
    service_data: UpdateService,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_service = await TypeServices.update_service(service_id, current_user, service_data, db)
    return updated_service


@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await TypeServices.delete_service(service_id, current_user, db)
    return result


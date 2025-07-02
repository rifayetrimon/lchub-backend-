from typing import List
from fastapi import APIRouter, Depends, status
from h11 import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.service_categories import CreateServiceCategory, ServiceCategory
from app.services.service_categories import ServiceCategoriesService

router = APIRouter(prefix="/service-categories", tags=["service-categories"])

@router.post("/create", response_model=ServiceCategory, status_code=status.HTTP_201_CREATED)
async def create_service_category(
    service_category_data: CreateServiceCategory,
    db: AsyncSession = Depends(get_db)
):
    # Call the service category creation method
    new_service_category = await ServiceCategoriesService.create_service_category(service_category_data, db)
    return new_service_category


@router.get("/", response_model=List[ServiceCategory], status_code=status.HTTP_200_OK)
async def get_service_categories(db: AsyncSession = Depends(get_db)):
    categories = await ServiceCategoriesService.get_service_categories(db)
    return categories


@router.get("/{id}", response_model=ServiceCategory, status_code=status.HTTP_200_OK)
async def get_service_category(id: int, db: AsyncSession = Depends(get_db)):
    category = await ServiceCategoriesService.get_service_category_by_id(id, db)

    return category


@router.put("/{id}", response_model=ServiceCategory, status_code=status.HTTP_200_OK)
async def update_service_category(id: int, service_category_data: ServiceCategory, db: AsyncSession = Depends(get_db)):
    updated_category = await ServiceCategoriesService.update_service_category(id, service_category_data, db)
    return updated_category



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_category(id: int, db: AsyncSession = Depends(get_db)):
    await ServiceCategoriesService.delete_service_category(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
from typing import List
from fastapi import APIRouter, Depends, status
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
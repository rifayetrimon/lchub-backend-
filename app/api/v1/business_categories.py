from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.business_categories import CreateBusinessCategories, ReadBusinessCategories
from fastapi import Depends, HTTPException, status
from app.services.business_categories import BusinessCategoriesService

router = APIRouter(prefix="/business", tags=["business"])

@router.post("/create", response_model=CreateBusinessCategories, status_code=status.HTTP_201_CREATED)
async def Create_business_categories(business_categories_data: CreateBusinessCategories, db: AsyncSession = Depends(get_db)):

    new_business_category = await BusinessCategoriesService.Create_business_category(business_categories_data, db)
    return new_business_category



@router.get("/", response_model=List[ReadBusinessCategories], status_code=status.HTTP_200_OK)
async def get_all_business_categories(db: AsyncSession = Depends(get_db)):
    categories = await BusinessCategoriesService.get_all_business_categories(db)
    return categories



from typing import List

from fastapi import APIRouter
from h11 import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.business_categories import CreateBusinessCategories, ReadBusinessCategories, UpdateBusinessCategories
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



@router.get("/{id}", response_model=ReadBusinessCategories, status_code=status.HTTP_200_OK)
async def get_business_category(id: int, db: AsyncSession = Depends(get_db)):
    category = await BusinessCategoriesService.get_business_category_by_id(id, db)
    return category



@router.put("/{id}", response_model=UpdateBusinessCategories, status_code=status.HTTP_200_OK)
async def update_business_category(id: int, business_category_data: UpdateBusinessCategories,db: AsyncSession = Depends(get_db)):
    update_category = await BusinessCategoriesService.update_business_category(id, business_category_data, db)
    return update_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business_category(id: int, db: AsyncSession = Depends(get_db)):
    await BusinessCategoriesService.delete_business_category(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

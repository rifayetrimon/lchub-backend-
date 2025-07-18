from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from h11 import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.job_categories import CreateJobCategory, ReadJobCategory, UpdateJobCategory
from app.services.job_categories import JobCategoriesService

router = APIRouter(prefix="/job_categories", tags=["job_categories"])

@router.post("/create", response_model=ReadJobCategory, status_code=status.HTTP_201_CREATED)
async def create_job_category(
    job_category_data: CreateJobCategory,
    db: AsyncSession = Depends(get_db)
):
    new_job_category = await JobCategoriesService.create_job_category(job_category_data, db)
    return new_job_category


@router.get("/", response_model=List[ReadJobCategory], status_code=status.HTTP_200_OK)
async def get_job_categories(skip: int = 0, db: AsyncSession = Depends(get_db)):
    job_categories = await JobCategoriesService.get_job_categories(db, skip=skip)
    return job_categories


@router.get("/{id}", response_model=ReadJobCategory, status_code=status.HTTP_200_OK)
async def get_job_category(id: int, db: AsyncSession = Depends(get_db)):
    job_category = await JobCategoriesService.get_job_category_by_id(id, db)
    return job_category



@router.put("/{id}", response_model=UpdateJobCategory, status_code=status.HTTP_200_OK)
async def update_job_category(id: int, job_category_data: UpdateJobCategory,db: AsyncSession = Depends(get_db)):
   update_job_category = await JobCategoriesService.update_job_category(id, job_category_data, db)
   return update_job_category



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_category(id: int, db: AsyncSession = Depends(get_db)):
    await JobCategoriesService.delete_job_category(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
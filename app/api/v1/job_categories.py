from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.job_categories import CreateJobCategory, ReadJobCategory
from app.services.job_categories import JobCategoriesService

router = APIRouter(prefix="/job_categories", tags=["job_categories"])

@router.post("/create", response_model=ReadJobCategory, status_code=status.HTTP_201_CREATED)
async def create_job_category(
    job_category_data: CreateJobCategory,
    db: AsyncSession = Depends(get_db)
):
    new_job_category = await JobCategoriesService.create_job_category(job_category_data, db)
    return new_job_category


@router.get("/", response_model=List[ReadJobCategory])
async def get_job_categories(db: AsyncSession = Depends(get_db)):
    job_categories = await JobCategoriesService.get_job_categories(db)
    return job_categories


@router.get("/{id}", response_model=ReadJobCategory)
async def get_job_category(id: int, db: AsyncSession = Depends(get_db)):
    job_category = await JobCategoriesService.get_job_category_by_id(id, db)
    return job_category
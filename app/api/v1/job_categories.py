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
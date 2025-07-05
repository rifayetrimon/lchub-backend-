from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.job import ServiceResponse, CreateJob, ReadJob, UpdateJob
from app.services.job import JobService


router = APIRouter(prefix="/job", tags=["job"])


@router.post("/create", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: CreateJob, db: AsyncSession = Depends(get_db), current_user : User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    new_job = await JobService.create_job(current_user, job, db)

    return new_job

@router.get("/", response_model=List[ReadJob])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    return await JobService.get_all_jobs(db)



@router.get("/{id}", response_model=ReadJob)
async def get_job_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await JobService.get_job_by_id(id, db)



@router.put("/update/{id}", response_model=ReadJob, status_code=status.HTTP_200_OK)
async def update_job(
    id: int,
    job: UpdateJob,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_job = await JobService.update_job(id, current_user, job, db)
    return updated_job



@router.delete("/{id}", response_model=ReadJob)
async def delete_job(id: int, db: AsyncSession = Depends(get_db)):
    job = await JobService.delete_job(id, db)
    return job

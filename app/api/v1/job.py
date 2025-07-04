from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.job import ServiceResponse, CreateJob
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


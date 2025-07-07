from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.users import User
from app.schemas.job_application import CreateJobApplication, ReadJobApplication
from app.services.job_application import JobApplicationService

router = APIRouter(prefix="/job-application", tags=["job-application"])



@router.post("/apply", response_model=ReadJobApplication, status_code=status.HTTP_201_CREATED)
async def create_job_application(
    job_application_data: CreateJobApplication,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    new_application = await JobApplicationService.create_job_application(db, job_application_data, user)
    return ReadJobApplication.model_validate(new_application)






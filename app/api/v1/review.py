from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.review import ReadReview, CreateReview
from app.services.review import ReviewService


router = APIRouter(prefix="/review", tags=["review"])

@router.post("/put", response_model=ReadReview, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: CreateReview,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    new_review = await ReviewService.put_review(user, review_data, db)
    return ReadReview.model_validate(new_review)



@router.get("/", response_model=List[ReadReview])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await ReviewService.get_review(db)
    return reviews
import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Service
from app.models.users import User
from app.models.reviews import Review
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.review import CreateReview

logger = logging.getLogger(__name__)

class ReviewService:

    @staticmethod
    async def _verify_user_authorization(user: User):
        if user.user_type not in ["student", "business"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user type",
            )

    @staticmethod
    async def put_review(user: User, review_data: CreateReview, db: AsyncSession):
        try:
            await ReviewService._verify_user_authorization(user)

            # Check if the user already reviewed this service
            existing = await db.execute(
                select(Review).where(
                    Review.user_id == user.id,
                    Review.service_id == review_data.service_id
                )
            )

            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already reviewed this service.",
                )

            new_review = Review(
                service_id=review_data.service_id,
                user_id=user.id,
                rating=review_data.rating,
                comment=review_data.comment,
            )

            db.add(new_review)
            await db.commit()
            await db.refresh(new_review)
            return new_review

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create review: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create review",
            )


    @staticmethod
    async def get_review(db: AsyncSession):
        try:
            review = await db.execute(
                select(Review)
            )
            all_reviews = review.scalars().all()

            if not all_reviews:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No reviews found",
                )

            return all_reviews

        except HTTPException as e:
            logger.error(f"Failed to get review: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get review",
            )
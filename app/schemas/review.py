from pydantic import BaseModel

class BaseReview(BaseModel):
    rating: float
    comment: str

class CreateReview(BaseReview):
    service_id: int

class ReadReview(BaseReview):
    id: int

    class Config:
        from_attributes = True
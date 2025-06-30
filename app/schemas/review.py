from pydantic import BaseModel



class BaseReview(BaseModel):
    rating: float
    comment: str


class CreateReview(BaseReview):
    pass

class UpdateReview(BaseReview):
    pass

class DeleteReview(BaseReview):
    pass

class ReadReview(BaseReview):
    id: int
    pass


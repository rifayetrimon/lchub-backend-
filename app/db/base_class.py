from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import  Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.operators import truediv


@as_declarative()
class Base:
    metadata = None
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



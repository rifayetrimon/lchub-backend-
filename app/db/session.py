import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

ssl_context = ssl.create_default_context()

# ✅ Create engine & session **inside get_db()**
async def get_db() -> AsyncSession:
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={"ssl": ssl_context},
        echo=False,  # Turn off for production
        future=True
    )

    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Optional: dispose engine if needed (safe cleanup)
    await engine.dispose()













# import ssl
# from fastapi import logger
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings



# ssl_context = ssl.create_default_context()

# # database engine
# engine = create_async_engine(
#     settings.DATABASE_URL,
#     connect_args={
#         "ssl": ssl_context
#     },
#     echo=True, future=True
# )


# # session maker
# async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# # get db session
# async def get_db():
#     async with async_session() as session:
#         yield session


# async def get_db():
#     async with async_session() as session:
#         logger.info(f"Session started: {id(session)}")
#         try:
#             yield session
#         finally:
#             logger.info(f"Session closed: {id(session)}")
import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

ssl_context = ssl.create_default_context()

# ✅ Use a function to create engine and session per request
async def get_db() -> AsyncSession:
    # 1️⃣ Create engine inside the request
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={"ssl": ssl_context},
        pool_size=5,  # Optional: set small pool size for Vercel
        max_overflow=0,
        echo=False,
        future=True
    )

    # 2️⃣ Create sessionmaker
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # 3️⃣ Yield session safely
    async with async_session() as session:
        try:
            yield session
        finally:
            # 4️⃣ Clean up engine explicitly (important in Vercel)
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
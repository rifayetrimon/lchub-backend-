from fastapi import FastAPI
import uvicorn
from app.db.session import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/health/db")
async def check_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "Connected!"}
    except Exception as e:
        import traceback
        return {"status": "Error!", "message": str(e), "trace": traceback.format_exc()}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
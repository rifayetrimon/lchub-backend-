import os
import sys
# Add the parent directory to Python path so we can import from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.db.session import engine
from sqlalchemy import text
from app.api.v1 import users, service, service_categories, job_categories, job, business_categories, job_application, review, emergency_contact

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}

# Include all your routers
app.include_router(users.router)
app.include_router(service.router)
app.include_router(service_categories.router)
app.include_router(job_categories.router)
app.include_router(job.router)
app.include_router(business_categories.router)
app.include_router(job_application.router)
app.include_router(review.router)
app.include_router(emergency_contact.router)

@app.get("/health/db")
async def check_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "Connected!"}
    except Exception as e:
        import traceback
        return {"status": "Error!", "message": str(e), "trace": traceback.format_exc()}
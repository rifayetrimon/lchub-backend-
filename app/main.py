import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import get_db
from sqlalchemy import text
from app.api.v1 import users, service, service_categories, job_categories, job, business_categories, job_application, review, emergency_contact


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
        async with get_db() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "Connected!"}
    except Exception as e:
        import traceback
        return {"status": "Error!", "message": str(e), "trace": traceback.format_exc()}



if __name__ == "__main__":
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    port = int(os.environ.get("PORT", 8000))  # Defaults to 8000 for local dev
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
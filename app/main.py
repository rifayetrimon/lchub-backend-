from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="8000", port=8000, reload=True)
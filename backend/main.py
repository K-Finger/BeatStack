from fastapi import FastAPI
from uploads.routes import router as upload_router

app = FastAPI()
app.include_router(upload_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
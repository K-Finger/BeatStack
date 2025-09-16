import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 1) your API first
from app.routers.uploads import router as uploads_router
from app.routers.auth import router as auth_router
# from app.routers.tags    import router as tags_router

# include routers
app.include_router(uploads_router, prefix="/api")
# app.include_router(tags_router)
app.include_router(auth_router, prefix="/auth")

# base dir for this file = BEATSTACK/app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2) serve index.html on GET /
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

# 3) mount everything under app/static at /static
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

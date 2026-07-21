from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.projects import router as projects_router

app = FastAPI(
    title="ForgeIQ",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)


@app.get("/")
def root():
    return {"message": "Welcome to ForgeIQ API!"}
from fastapi import FastAPI
from app.routers import preferences, content, mlb_data
from db import database, async_engine, Base
from app.users import fastapi_users, auth_backend
from app.models.user import UserCreate, UserUpdate, UserRead

# FastAPI App
app = FastAPI()

# Include authentication routes
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

# Include other routers
app.include_router(preferences.router, prefix="/api/preferences")
app.include_router(content.router, prefix="/api/content")
app.include_router(mlb_data.router, prefix="/api/mlb_data")

@app.on_event("startup")
async def on_startup():
    await database.connect()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Personalized Fan Highlights API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

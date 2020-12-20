from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Routers
from src.routers import router as item_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Init MongoDB connections on startup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]
    if settings.DEBUG_MODE:
        print(f"DEBUG mode ON! DO NOT USE DEBUG_MODE={settings.DEBUG_MODE} IN PRODUCTION!")
        print("SETTINGS:")
        print(f"MONGODB_URL={settings.MONGODB_URL}")
        print(f"DB_NAME={settings.MONGODB_DB_NAME}")


# Terminate MongoDB connections on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Add routers
app.include_router(item_router, tags=["items"], prefix="/api/v1/items")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        reload=settings.DEBUG_MODE,
        port=settings.APP_PORT,
    )

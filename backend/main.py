from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import connect_to_mongo, close_mongo_connection
from backend.routers import contact

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Contact List API",
    description="A simple FastAPI application for managing contacts with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(contact.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Contact List API", "docs": "/docs"}
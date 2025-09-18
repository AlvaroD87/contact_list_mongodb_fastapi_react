from motor.motor_asyncio import AsyncIOMotorClient  # pyright: ignore[reportMissingImports]
from backend.config import config

# MongoDB connection settings
MONGODB_URL = config.DATABASE_URL
DATABASE_NAME = config.DATABASE_NAME

# Global variable to store the database connection
client = None
database = None

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DATABASE_NAME]
        # Test the connection
        await client.admin.command('ping')
        print(f"Connected to MongoDB at {MONGODB_URL}")
        print(f"Using database: {DATABASE_NAME}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return database

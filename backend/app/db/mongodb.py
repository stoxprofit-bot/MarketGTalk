from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

client: AsyncIOMotorClient | None = None
db = None


async def connect_to_mongo() -> None:
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]


async def close_mongo_connection() -> None:
    global client
    if client is not None:
        client.close()


def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("MongoDB connection has not been initialized")
    return db

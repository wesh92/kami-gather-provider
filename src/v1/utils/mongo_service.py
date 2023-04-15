from motor.motor_asyncio import AsyncIOMotorClient


def mongo_get_collection(
    connection_string: str, db_name: str, collection_name: str
) -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(connection_string)
    db = client[db_name]
    return db[collection_name]

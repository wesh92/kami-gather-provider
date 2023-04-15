from motor.motor_asyncio import AsyncIOMotorClient


def mongo_connect(connection_string: str) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(connection_string)

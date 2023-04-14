from surrealdb import Surreal


async def connect_to_db() -> Surreal:
    db = Surreal("ws://localhost:8000/rpc")
    await db.connect()
    await db.signin({"user": "root", "pass": "root"})
    return db

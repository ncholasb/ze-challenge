from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"


client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["mydatabase"]
partners_collection = db["partners"]


async def connect_to_mongo():
    pass


async def close_mongo_connection():
    pass

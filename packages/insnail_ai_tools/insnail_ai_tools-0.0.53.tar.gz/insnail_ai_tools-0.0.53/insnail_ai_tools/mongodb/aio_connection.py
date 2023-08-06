from asyncio.base_events import BaseEventLoop

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

aio_mongo_client: AsyncIOMotorClient = None
aio_mongo_database: AsyncIOMotorDatabase = None


def init_mongodb_connection_async(
    loop: BaseEventLoop,
    mongo_uri: str,
    database: str,
):
    global aio_mongo_client
    global aio_mongo_database
    aio_mongo_client = AsyncIOMotorClient(mongo_uri, io_loop=loop)
    aio_mongo_database = aio_mongo_client[database]

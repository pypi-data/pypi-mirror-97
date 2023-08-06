from enum import Enum, IntEnum
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorCollection


class StrChoicesMixin(str, Enum):
    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls.__members__.values()]


class IntChoicesMixin(IntEnum):
    @classmethod
    def choices(cls):
        return [(i.value, i.name) for i in cls.__members__.values()]


class AioMixin:
    """
    需要使用实现aio操作的 mongo document 请集成此类
    """

    @classmethod
    @lru_cache(maxsize=32)
    def get_aio_collection(cls) -> AsyncIOMotorCollection:
        from insnail_ai_tools.mongodb.aio_connection import aio_mongo_database

        assert aio_mongo_database, "未初始化 aio mongo的连接"
        return aio_mongo_database[cls._meta["collection"]]


class MultiDatabaseMixin:
    @classmethod
    def set_connect(cls, alias: str = "default"):
        """设置多库连接"""
        cls._meta["db_alias"] = alias

    @classmethod
    def deactivate_abstract(cls):
        """取消抽象类"""
        cls._meta["abstract"] = False


class MongoCanalKafkaMixin:
    """mongoengine 的类，需要使用 canal-kafka 功能的，可以继承此类"""

    @classmethod
    @lru_cache(maxsize=256)
    def get_id_field(cls) -> str:
        return cls._meta["id_field"]

    @classmethod
    async def create_or_update_object_from_kafka_data(cls, data: dict):
        data = cls.clean_kafka_data(data)
        id_params = {cls.get_id_field(): data[cls.get_id_field()]}
        obj = cls.objects.filter(**id_params).first() or cls(**id_params)

        for k, v in data.items():
            obj[k] = v
        obj.save()
        return obj

    @classmethod
    async def delete_from_kafka_data(cls, data: dict):
        id_params = {cls.get_id_field(): data[cls.get_id_field()]}
        cls.objects.filter(**id_params).delete()

    @classmethod
    def clean_kafka_data(cls, data: dict) -> dict:
        if "#alibaba_rds_row_id#" in data:
            del data["#alibaba_rds_row_id#"]
        return data

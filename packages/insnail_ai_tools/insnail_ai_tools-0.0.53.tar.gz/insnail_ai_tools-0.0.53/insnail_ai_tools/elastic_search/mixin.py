from functools import lru_cache

from elasticsearch.exceptions import NotFoundError


class AioMixin:
    @classmethod
    async def aio_search(cls, *args, **kwargs):
        from insnail_ai_tools.elastic_search.aio_connection import aio_elastic_search

        assert aio_elastic_search, "未初始化 aio es的连接"
        search = await aio_elastic_search.search(index=cls.Index.name, *args, **kwargs)
        return search

    @classmethod
    async def aio_get(cls, _id):
        from insnail_ai_tools.elastic_search.aio_connection import aio_elastic_search

        assert aio_elastic_search, "未初始化 aio es的连接"
        return await aio_elastic_search.get(index=cls.Index.name, id=_id)


class MongoSyncMixin:
    @classmethod
    def create_or_update_from_mongo(cls, data: dict, save: bool = True):
        properties: dict = cls._doc_type.mapping.properties.to_dict().get(
            "properties", {}
        )
        _id = data.pop("_id")
        try:
            obj = cls.get(id=_id)
        except NotFoundError:
            obj = cls()
            obj.meta.id = _id
        for k, v in data.items():
            if k in properties:
                obj[k] = v
        if save:
            obj.save()
        return obj

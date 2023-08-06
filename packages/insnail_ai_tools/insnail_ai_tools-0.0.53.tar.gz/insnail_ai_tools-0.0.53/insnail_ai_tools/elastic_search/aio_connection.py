from asyncio.base_events import BaseEventLoop

from elasticsearch._async.client import AsyncElasticsearch

aio_elastic_search: AsyncElasticsearch


def init_elastic_search_async(
    loop: BaseEventLoop,
    es_uri,
):
    global aio_elastic_search
    aio_elastic_search = AsyncElasticsearch(hosts=es_uri, loop=loop)

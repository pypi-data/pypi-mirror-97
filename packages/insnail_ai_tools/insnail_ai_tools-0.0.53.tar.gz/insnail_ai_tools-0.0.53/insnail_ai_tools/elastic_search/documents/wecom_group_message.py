from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Document, InnerDoc
from elasticsearch_dsl.analysis import analyzer
from elasticsearch_dsl.field import (
    AttrDict,
    Boolean,
    Date,
    Float,
    Integer,
    Keyword,
    Nested,
    Object,
    Text,
)
from elasticsearch_dsl.query import Q

from insnail_ai_tools.elastic_search.analyzer import word_analyzer
from insnail_ai_tools.elastic_search.mixin import AioMixin


class WecomGroupMessageIndex(Document, AioMixin):
    msg_id = Keyword()
    room_id = Keyword()
    from_user_id = Keyword()
    msg_type = Keyword()
    to_list = Keyword()
    action = Keyword()

    content = Object()
    content_text = Text(analyzer=word_analyzer)
    url = Text()

    msg_time = Date()
    create_time = Date()

    class Index:
        name = "wecom_group_message"

    @classmethod
    def create_or_update_from_mongo(cls, data: dict):
        try:
            wm = cls.get(id=data["msg_id"])
        except NotFoundError:
            wm = cls()
            wm.meta.id = data["msg_id"]

        for k, v in data.items():
            if k == "_id":
                continue
            if k == "extra":
                for k2, v2 in v.items():
                    wm[k2] = v2
            else:
                wm[k] = v
        return wm

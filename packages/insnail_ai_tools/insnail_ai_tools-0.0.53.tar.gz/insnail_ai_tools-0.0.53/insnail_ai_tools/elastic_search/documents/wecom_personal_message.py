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
from insnail_ai_tools.elastic_search.mixin import AioMixin, MongoSyncMixin


class WecomPersonalMessageIndex(Document, AioMixin, MongoSyncMixin):
    msg_id = Keyword()
    action = Keyword()
    msg_type = Keyword()
    from_user_id = Keyword()
    to_user_id = Keyword()
    unionid = Keyword()

    content = Object()
    content_text = Text(analyzer=word_analyzer)
    url = Text()

    msg_time = Date()
    create_time = Date()

    class Index:
        name = "wecom_personal_message"

    async def get_dialog_context(self, limit: int = 10):
        query = Q("term", user_id=self.user_id[0]) & Q(
            "term", external_user_id=self.external_user_id[0]
        )

        pre_query = query & Q(
            "range",
            msg_time={
                "lt": self.msg_time.strftime("%Y-%m-%d %H:%M:%S"),
                "format": "yyyy-MM-dd HH:mm:ss",
            },
        )

        post_query = query & Q(
            "range",
            msg_time={
                "gt": self.msg_time.strftime("%Y-%m-%d %H:%M:%S"),
                "format": "yyyy-MM-dd HH:mm:ss",
            },
        )

        pre_data = (
            WecomPersonalMessageIndex.search()
            .query(pre_query)
            .sort("-msg_time")[:limit]
            .execute()
        )
        post_data = (
            WecomPersonalMessageIndex.search()
            .query(post_query)
            .sort("msg_time")[:limit]
            .execute()
        )
        results = []
        for i in reversed(pre_data.hits):
            results.append(i.to_dict())
        results.append(self.to_dict())
        for i in post_data.hits:
            results.append(i.to_dict())
        return results

from elasticsearch_dsl import Document

from insnail_ai_tools.elastic_search.mixin import AioMixin
from insnail_ai_tools.elastic_search.mongodb_plugin import MongoToEs
from insnail_ai_tools.mongodb.model.wecom.group_chat import WecomExternalGroupChat


@MongoToEs(
    WecomExternalGroupChat,
    fields=["chat_id", "name", "owner", "notice", "is_delete", "create_time"],
)
class WecomExternalGroupChatIndex(Document, AioMixin):
    class Index:
        name = "wecom_group_chat"

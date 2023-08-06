from elasticsearch_dsl import Document
from elasticsearch_dsl.field import Text

from insnail_ai_tools.elastic_search.mixin import AioMixin
from insnail_ai_tools.elastic_search.mongodb_plugin import MongoToEs
from insnail_ai_tools.mongodb.model.wecom.user import WecomUser


@MongoToEs(
    WecomUser,
    fields=["userid", "name", "mobile", "department", "position", "email", "is_delete"],
)
class WecomUserIndex(Document, AioMixin):
    class Index:
        name = f"wecom_user"

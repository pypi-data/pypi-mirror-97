from elasticsearch_dsl import Document

from insnail_ai_tools.elastic_search.mixin import AioMixin
from insnail_ai_tools.elastic_search.mongodb_plugin import MongoToEs
from insnail_ai_tools.mongodb.model.wecom.external_user import WecomExternalUser


@MongoToEs(
    WecomExternalUser,
    fields=["external_userid", "name", "type", "gender", "unionid", "is_delete"],
)
class WecomExternalUserIndex(Document, AioMixin):
    class Index:
        name = "wecom_external_user"

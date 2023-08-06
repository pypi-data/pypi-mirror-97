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

from insnail_ai_tools.elastic_search.mixin import AioMixin, MongoSyncMixin


class WecomUserRelationIndex(Document, AioMixin, MongoSyncMixin):
    userid = Keyword()
    external_userid = Keyword()
    remark = Text()
    description = Text()
    createtime = Date()
    tag_id = Keyword()
    remark_corp_name = Text()
    remark_mobiles = Keyword()
    add_way = Keyword()
    oper_userid = Keyword()
    state = Keyword()
    is_delete = Boolean()

    class Index:
        name = "wecom_user_relation"

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


class CallCenterVoiceMeta(InnerDoc):
    start_time = Integer()
    end_time = Integer()
    text = Text()
    from_role = Keyword()


class CallCenterIndex(Document, AioMixin):
    start_time = Date()
    end_time = Date()
    customer_id = Keyword()
    customer_name = Keyword()
    talk_time = Keyword()
    call_type = Keyword()
    usr_user_id = Keyword()
    mkt_user_id = Keyword()
    user_phone = Keyword()
    record_url = Keyword()
    contact_id = Keyword()
    qa_score = Integer()
    connid = Keyword()
    username = Keyword()
    contact_disposition = Keyword()
    update_qauality_check_phrase = Keyword()
    quality_check_phrase = Nested(CallCenterVoiceMeta)

    class Index:
        name = "call_center"

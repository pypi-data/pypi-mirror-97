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


class WecomMeetingVoiceMeta(InnerDoc):
    start_time = Integer()
    end_time = Integer()
    text = Text()
    from_role = Keyword()


class WecomMeetingVoiceIndex(Document, AioMixin):
    msg_id = Keyword()
    user_id = Keyword()
    external_user_id = Keyword()
    union_id = Keyword()
    talk_time = Integer()
    call_type = Integer()
    start_time = Date()
    end_time = Date()
    url = Text()
    create_time = Date()
    asr_status = Integer()

    messages = Nested(WecomMeetingVoiceMeta)

    class Index:
        name = "wecom_meeting_voice"

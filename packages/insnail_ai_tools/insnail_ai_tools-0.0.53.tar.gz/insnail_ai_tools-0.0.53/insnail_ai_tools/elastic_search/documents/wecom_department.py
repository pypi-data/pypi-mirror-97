from elasticsearch_dsl import Document

from insnail_ai_tools.elastic_search.mixin import AioMixin
from insnail_ai_tools.elastic_search.mongodb_plugin import MongoToEs
from insnail_ai_tools.mongodb.model.wecom.department import WecomDepartment


@MongoToEs(WecomDepartment)
class WecomDepartmentIndex(Document, AioMixin):
    class Index:
        name = "wecom_department"

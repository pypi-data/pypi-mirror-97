import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin

DEPARTMENT_ID_KEY = "_id"
DEPARTMENTS_KEY = "departments"
PARENT_ID_KEY = "parentid"


class WecomDepartment(mongoengine.DynamicDocument, MultiDatabaseMixin):
    id = mongoengine.IntField(
        primary_key=True,
        verbose_name="部门id",
        help_text="部门id，32位整型，指定时必须大于1。若不填该参数，将自动生成id",
    )

    name = mongoengine.StringField(
        required=True,
        verbose_name="部门名称",
        help_text=r"部门名称。同一个层级的部门名称不能重复。长度限制为1~32个字符，字符不能包括\:?”<>｜",
        max_length=32,
    )
    name_en = mongoengine.StringField(
        required=False,
        verbose_name="英文名称",
        help_text=r"英文名称。同一个层级的部门名称不能重复。需要在管理后台开启多语言支持才能生效。长度限制为1~32个字符，字符不能包括\:?”<>｜",
    )
    parentid = mongoengine.IntField(
        required=True,
        verbose_name="父部门id",
        help_text="父部门id，32位整型",
        reference="wecom_department",
    )
    order = mongoengine.IntField(
        required=False,
        verbose_name="在父部门中的次序值",
        help_text="在父部门中的次序值。order值大的排序靠前。有效的值范围True[0, 2^32)",
    )
    is_delete = mongoengine.BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )

    meta = {
        "collection": "wecom_department",
        "indexes": [
            "#name",
            "name_en",
            "#parentid",
            "#order",
        ],
        "abstract": True,
    }

    def __str__(self):
        return self.name

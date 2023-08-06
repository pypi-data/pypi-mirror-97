from typing import Dict, List

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin, StrChoicesMixin


class TaskType(StrChoicesMixin):
    SCHEDULE = "日程安排"


class TaskStatus(StrChoicesMixin):
    INIT = "创建"
    CANCEL = "取消"
    COMPLETE = "完成"


class TaskCallback(StrChoicesMixin):
    AFFIRM = "确认"
    CANCEL = "取消"

    @classmethod
    def get_buttons(cls) -> List[Dict]:
        return [
            {
                "key": cls.CANCEL.name,
                "name": cls.CANCEL.value,
                "replace_name": f"已{cls.CANCEL.value}",
                "color": "blue",
            },
            {
                "key": cls.AFFIRM.name,
                "name": cls.AFFIRM.value,
                "replace_name": f"已{cls.AFFIRM.value}",
                "color": "blue",
                "is_bold": True,
            },
        ]


class CommTask(mongoengine.DynamicDocument, MultiDatabaseMixin):
    user_id = mongoengine.StringField(verbose_name="企业微信用户ID")
    type = mongoengine.StringField(verbose_name="task类型", choices=TaskType.choices())
    status = mongoengine.StringField(
        verbose_name="task目前的状态", choices=TaskStatus.choices()
    )
    content = mongoengine.DictField(verbose_name="task具体内容")
    create_time = mongoengine.DateTimeField(verbose_name="创建时间")

    meta = {
        "collection": "comm_task",
        "indexes": ["#msg_id", "#source", "#type", "create_time"],
        "abstract": True,
    }

    def __str__(self):
        return f"{self.user_id}-{self.type}-{self.status}"

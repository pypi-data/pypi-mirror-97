import datetime

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class WecomGroupChatMember(mongoengine.DynamicEmbeddedDocument):
    userid = mongoengine.StringField(verbose_name="群成员id")
    type = mongoengine.IntField(
        verbose_name="成员类型",
        choices=((1, "企业成员2"), (2, "外部联系人")),
        help_text="成员类型。1 - 企业成员2 - 外部联系人",
    )
    unionid = mongoengine.StringField(
        verbose_name="群成员id",
        help_text="外部联系人在微信开放平台的唯一身份标识（微信unionid），通过此字段企业可将外部联系人与公众号/小程序用户关联起来。",
    )
    join_time = mongoengine.DateTimeField(verbose_name="入群时间")
    join_scene = mongoengine.IntField(
        verbose_name="入群方式。",
        choices=(
            (0, "未知"),
            (1, "由成员邀请入群（直接邀请入群）"),
            (2, "由成员邀请入群（通过邀请链接入群）"),
            (3, "通过扫描群二维码入群"),
        ),
    )

    @classmethod
    def from_server_data(cls, data: dict) -> "WecomGroupChatMember":
        if isinstance(data["join_time"], int):
            data["join_time"] = datetime.datetime.fromtimestamp(data["join_time"])
        return cls._from_son(data)


class WecomExternalGroupChat(mongoengine.DynamicDocument, MultiDatabaseMixin):
    chat_id = mongoengine.StringField(
        verbose_name="客户群ID",
        unique=True,
        required=True,
    )
    name = mongoengine.StringField(verbose_name="群名")
    owner = mongoengine.StringField(verbose_name="群主ID")
    notice = mongoengine.StringField(verbose_name="notice")
    member_list = mongoengine.EmbeddedDocumentListField(
        WecomGroupChatMember, verbose_name="成员列表"
    )
    is_delete = mongoengine.BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )
    create_time = mongoengine.DateTimeField(verbose_name="群的创建时间", help_text="群的创建时间")

    meta = {
        "collection": "wecom_external_group_chat",
        "indexes": [
            "#chat_id",
            "name",
            "#owner",
            "is_delete",
            "create_time",
        ],
        "abstract": True,
    }

    def __str__(self):
        return self.name

from mongoengine import (
    BooleanField,
    DynamicDocument,
    EmbeddedDocumentField,
    IntField,
    StringField,
)

from insnail_ai_tools.mongodb.mixin import IntChoicesMixin, MultiDatabaseMixin

from .meta import WecomUserExternalProfile


class WecomExternalUserGender(IntChoicesMixin):
    UNKNOWN = 0
    MAN = 1
    WOMEN = 2


class WecomExternalUserType(IntChoicesMixin):
    WECHAT = 1
    WECOM = 2


class WecomExternalUser(DynamicDocument, MultiDatabaseMixin):
    external_userid = StringField(
        verbose_name="外部联系人的userid", help_text="企业员工添加的客户userid", primary_key=True
    )
    name = StringField(
        verbose_name="外部联系人的名称",
        help_text="如果外部联系人为微信用户，则返回外部联系人的名称为其微信昵称；如果外部联系人为企业微信用户，则会按照以下优先级顺序返回：此外部联系人或管理员设置的昵称、认证的实名和账号名称。",
        required=True,
    )
    avatar = StringField(verbose_name="外部联系人头像url", help_text="外部联系人头像url，第三方不可获取")
    type = IntField(
        verbose_name="外部联系人的类型",
        help_text="外部联系人的类型，1表示该外部联系人是微信用户，2表示该外部联系人是企业微信用户",
        choices=WecomExternalUserType.choices(),
    )
    gender = IntField(
        verbose_name="外部联系人性别",
        help_text="外部联系人性别 0-未知 1-男性 2-女性",
        choices=WecomExternalUserGender.choices(),
    )
    unionid = StringField(
        verbose_name="外部联系人在微信开放平台的唯一身份标识（微信unionid）",
        help_text="外部联系人在微信开放平台的唯一身份标识（微信unionid），通过此字段企业可将外部联系人与公众号/小程序用户关联起来。仅当联系人类型是微信用户，且企业或第三方服务商绑定了微信开发者ID有此字段。",
        max_length=64,
    )
    position = StringField(
        verbose_name="外部联系人的职位",
        help_text="外部联系人的职位，如果外部企业或用户选择隐藏职位，则不返回，仅当联系人类型是企业微信用户时有此字段",
    )
    corp_name = StringField(
        verbose_name="外部联系人所在企业的简称", help_text="外部联系人所在企业的简称，仅当联系人类型是企业微信用户时有此字段"
    )
    corp_full_name = StringField(
        verbose_name="外部联系人所在企业的主体名称", help_text="外部联系人所在企业的主体名称，仅当联系人类型是企业微信用户时有此字段"
    )
    external_profile = EmbeddedDocumentField(
        WecomUserExternalProfile,
        verbose_name="外部联系人的自定义展示信息",
        help_text="外部联系人的自定义展示信息，可以有多个字段和多种类型，包括文本，网页和小程序，仅当联系人类型是企业微信用户时有此字段",
    )

    is_delete = BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )

    def __str__(self):
        return self.name

    meta = {
        "collection": "wecom_external_user",
        "indexes": [
            "#external_userid",
            "name",
            "#unionid",
            "#gender",
            "#status",
            "is_delete",
        ],
        "abstract": True,
    }

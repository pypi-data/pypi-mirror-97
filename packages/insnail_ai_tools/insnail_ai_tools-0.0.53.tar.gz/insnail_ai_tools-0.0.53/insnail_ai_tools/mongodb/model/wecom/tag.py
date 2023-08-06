import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class TagInfo(mongoengine.DynamicDocument, MultiDatabaseMixin):
    group_id = mongoengine.StringField(
        verbose_name="企业成员添加此外部联系人所打标签的分组id",
        help_text="企业成员添加此外部联系人所打标签的分组id（标签功能需要企业微信升级到2.7.5及以上版本）",
    )
    group_name = mongoengine.StringField(
        verbose_name="企业成员添加此外部联系人所打标签的分组名称",
        help_text="企业成员添加此外部联系人所打标签的分组名称（标签功能需要企业微信升级到2.7.5及以上版本）",
    )
    tag_name = mongoengine.StringField(
        verbose_name="企业成员添加此外部联系人所打标签名称", help_text="企业成员添加此外部联系人所打标签名称"
    )
    type = mongoengine.IntField(
        verbose_name="企业成员添加此外部联系人所打标签类型",
        help_text="企业成员添加此外部联系人所打标签类型, 1-企业设置, 2-用户自定义",
    )
    tag_id = mongoengine.StringField(
        verbose_name="企业成员添加此外部联系人所打企业标签的id",
        help_text="企业成员添加此外部联系人所打企业标签的id，仅企业设置（type为1）的标签返回",
    )
    is_delete = mongoengine.BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )

    def __str__(self):
        return self.tag_name

    meta = {
        "collection": "wecom_tag_info",
        "indexes": ["#group_id", "#tag_name", "type", "#tag_id", "is_delete"],
        "abstract": True,
    }

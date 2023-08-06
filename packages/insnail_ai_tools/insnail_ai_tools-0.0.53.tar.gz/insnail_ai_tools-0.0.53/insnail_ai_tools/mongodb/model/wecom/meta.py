import mongoengine

from insnail_ai_tools.mongodb.mixin import StrChoicesMixin


class AttrText(mongoengine.EmbeddedDocument):
    value = mongoengine.StringField(
        verbose_name="文本属性内容", help_text="文本属性内容,长度限制12个UTF8字符"
    )

    def __str__(self):
        return self.value


class AttrWeb(mongoengine.EmbeddedDocument):
    url = mongoengine.StringField(
        verbose_name="网页的url", help_text="网页的url,必须包含http或者https头"
    )
    title = mongoengine.StringField(
        verbose_name="网页的展示标题", help_text="网页的展示标题,长度限制12个UTF8字符"
    )

    def __str__(self):
        return self.title


class AttrMiniProgram(mongoengine.EmbeddedDocument):
    appid = mongoengine.StringField(
        verbose_name="小程序appid", help_text="小程序appid，必须是有在本企业安装授权的小程序，否则会被忽略"
    )
    title = mongoengine.StringField(
        verbose_name="小程序的展示标题", help_text="小程序的展示标题,长度限制12个UTF8字符"
    )
    pagepath = mongoengine.StringField(verbose_name="小程序的页面路径", help_text="小程序的页面路径")

    def __str__(self):
        return f"{self.appid}-{self.title}"


class WecomUserExternalAttr(mongoengine.DynamicEmbeddedDocument):
    type = mongoengine.IntField(verbose_name="属性类型", help_text="属性类型: 0-文本 1-网页 2-小程序")
    name = mongoengine.StringField(
        verbose_name="属性名称", help_text="属性名称：需要先确保在管理端有创建该属性，否则会忽略"
    )
    text = mongoengine.EmbeddedDocumentField(
        AttrText, verbose_name="文本类型的属性", help_text="文本类型的属性"
    )
    web = mongoengine.EmbeddedDocumentField(
        AttrWeb,
        verbose_name="网页类型的属性",
        help_text="网页类型的属性，url和title字段要么同时为空表示清除该属性，要么同时不为空",
    )
    miniprogram = mongoengine.EmbeddedDocumentField(
        AttrMiniProgram,
        verbose_name="小程序类型的属性",
        help_text="小程序类型的属性，appid和title字段要么同时为空表示清除该属性，要么同时不为空",
    )

    def __str__(self):
        return f"{self.name}"


class WecomUserExternalProfile(mongoengine.DynamicEmbeddedDocument):
    external_corp_name = mongoengine.StringField(
        verbose_name="企业对外简称", help_text="企业对外简称，需从已认证的企业简称中选填。可在“我的企业”页中查看企业简称认证状态。"
    )

    external_attr = mongoengine.EmbeddedDocumentListField(
        WecomUserExternalAttr, verbose_name="属性列表", help_text="属性列表，目前支持文本、网页、小程序三种类型"
    )

    def __str__(self):
        return self.external_corp_name


class WecomMessageActionChoices(StrChoicesMixin):
    send = "发送"
    recall = "撤回"
    switch = "切换企业日志"

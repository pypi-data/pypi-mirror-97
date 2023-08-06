from wechatpy import events
from wechatpy.fields import StringField
from wechatpy.work.events import register_event


@register_event("change_external_chat")
class ChangeExternalChatEvent(events.BaseEvent):
    """
    客户群事件
    enum change_type:
        create: 客户群创建事件
        update: 客户群变更事件
        dismiss: 客户群解散事件
    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/92130#%E6%B7%BB%E5%8A%A0%E4%BC%81%E4%B8%9A%E5%AE%A2%E6%88%B7%E4%BA%8B%E4%BB%B6
    """

    event = "change_external_chat"
    #
    change_type = StringField("ChangeType")
    chat_id = StringField("ChatId")


@register_event("change_external_tag")
class ChangeExternalTagEvent(events.BaseEvent):
    """
    客户群事件
    enum change_type:
        create: 企业客户标签创建事件
        update: 企业客户标签变更事件
        dismiss: 企业客户标签删除事件
    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/92130#%E6%B7%BB%E5%8A%A0%E4%BC%81%E4%B8%9A%E5%AE%A2%E6%88%B7%E4%BA%8B%E4%BB%B6
    """

    event = "change_external_tag"
    tag_id = StringField("Id")
    # 创建标签时，此项为tag，创建标签组时，此项为tag_group
    tag_type = StringField("TagType")
    change_type = StringField("ChangeType")

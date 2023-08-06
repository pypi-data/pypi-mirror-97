import mongoengine

from insnail_ai_tools.mongodb.mixin import AioMixin, MultiDatabaseMixin, StrChoicesMixin


class WecomEventChoice(StrChoicesMixin):
    """企业微信的所有事件"""

    subscribe = "用户关注事件"
    unsubscribe = "用户取消关注事件"
    click = "点击菜单拉取消息事件"
    view = "点击菜单跳转链接事件"
    location = "上报地理位置事件"
    scancode_push = "扫码推事件的事件"
    scancode_waitmsg = "扫码推事件且弹出“消息接收中”提示框的事件"
    pic_sysphoto = "弹出系统拍照发图事件"
    pic_photo_or_album = "弹出拍照或相册发图事件"
    pic_weixin = "弹出微信相册发图器事件"
    location_select = "弹出地理位置选择器事件"
    enter_agent = "用户进入应用的事件推送"
    batch_job_result = "异步任务完成事件"
    open_approval_change = "审批状态通知事件"
    taskcard_click = "任务卡片事件推送"
    change_external_contact = "外部联系人变更事件"


class WecomChangeExternalContactChangeTypeChoices(StrChoicesMixin):
    """企业微信-外部联系人变更事件 中的所有变更类型"""

    add_external_contact = "添加企业客户"
    edit_external_contact = "编辑企业客户"
    add_half_external_contact = "外部联系人免验证添加成员"
    del_external_contact = "删除企业客户"
    del_follow_user = "删除跟进成员"
    transfer_fail = "客户接替失败"


class WecomEventMessageType(StrChoicesMixin):
    """企业微信 message event的所有类型"""

    text = "文本"
    image = "图片"
    voice = "语音"
    shortvideo = "短视频"
    video = "视频"
    location = "位置"
    link = "链接"


class WecomEvent(mongoengine.DynamicDocument, AioMixin, MultiDatabaseMixin):
    # 基础的事件表，所有接收到的事件都会存储起来, 未做结构化
    event = mongoengine.StringField(
        verbose_name="事件类型", choices=WecomEventChoice.choices()
    )
    content = mongoengine.DictField(verbose_name="事件的内容")

    meta = {
        "collection": "wecom_event",
        "indexes": ["#event"],
        "abstract": True,
    }

    def __str__(self):
        return self.event


class WecomChangeExternalContactEvent(
    mongoengine.DynamicDocument, AioMixin, MultiDatabaseMixin
):
    # 联系人变更事件 单独存放一张表，做了部分结构化
    event = mongoengine.StringField(
        verbose_name="事件类型", default="change_external_contact"
    )
    change_type = mongoengine.StringField(
        verbose_name="变更类型",
        choices=WecomChangeExternalContactChangeTypeChoices.choices(),
    )
    welcome_code = mongoengine.StringField(verbose_name="欢迎语code", max_length=64)
    state = mongoengine.StringField(
        verbose_name="「联系我」参数",
        help_text="添加此用户的「联系我」方式配置的state参数，可用于识别添加此用户的渠道",
        max_length=30,
    )

    user_id = mongoengine.StringField(
        verbose_name="用户ID",
        help_text="添加了外部联系人(客户)的企业成员userid",
        max_length=64,
        reference="wecom_user",
    )
    external_user_id = mongoengine.StringField(
        verbose_name="客户ID",
        help_text="企业员工添加的客户userid",
        max_length=64,
        reference="wecom_external_user",
    )
    create_time = mongoengine.DateTimeField(verbose_name="消息创建时间 ")

    meta = {
        "collection": "wecom_change_external_contact_event",
        "indexes": [
            "msg_id",
            "#event",
            "#change_type",
            "#state",
            "#user_id",
            "#external_user_id",
            "create_time",
        ],
        "abstract": True,
    }

    def __str__(self):
        return getattr(
            WecomChangeExternalContactChangeTypeChoices, self.change_type
        ).value


class WecomEventMessage(mongoengine.DynamicDocument, AioMixin, MultiDatabaseMixin):
    # 企业微信 消息类 事件。即客户在agent中发送的消息，都会存储在此
    msg_id = mongoengine.IntField(verbose_name="消息的ID")
    type = mongoengine.StringField(
        verbose_name="消息类型", choices=WecomEventMessageType.choices()
    )

    source = mongoengine.StringField(verbose_name="消息发送人")
    target = mongoengine.StringField(verbose_name="接收人")

    agent = mongoengine.IntField(verbose_name="APP ID")
    content = mongoengine.DictField(verbose_name="消息内容")

    create_time = mongoengine.DateTimeField(verbose_name="消息创建时间 ")

    meta = {
        "collection": "wecom_event_message",
        "indexes": ["#msg_id", "#source", "#type", "create_time"],
        "abstract": True,
    }

    def __str__(self):
        return self.type

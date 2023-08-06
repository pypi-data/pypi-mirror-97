import mongoengine

from insnail_ai_tools.mongodb.mixin import IntChoicesMixin, MultiDatabaseMixin


class ContactWayType(IntChoicesMixin):
    SINGLE = 1
    MANY = 2


class ContactWayScene(IntChoicesMixin):
    MINI_PROGRAM = 1
    QR_CODE = 2


class ContactWay(mongoengine.DynamicDocument, MultiDatabaseMixin):
    config_id = mongoengine.StringField(
        verbose_name="企业联系方式的配置id", help_text="企业联系方式的配置id", primary_key=True
    )
    state = mongoengine.StringField(
        verbose_name="企业自定义的state参数",
        help_text="企业自定义的state参数，用于区分不同的添加渠道，在调用“获取外部联系人详情”时会返回该参数值，不超过30个字符",
        max_length=30,
    )
    type = mongoengine.IntField(
        verbose_name="联系方式类型",
        choices=ContactWayType.choices(),
        help_text="联系方式类型,1-单人, 2-多人",
        required=True,
    )
    scene = mongoengine.IntField(
        verbose_name="场景",
        choices=ContactWayScene.choices(),
        help_text="场景，1-在小程序中联系，2-通过二维码联系",
        required=True,
    )
    style = mongoengine.IntField(
        verbose_name="在小程序中联系时使用的控件样式", help_text="在小程序中联系时使用的控件样式，详见附表"
    )
    remark = mongoengine.StringField(
        verbose_name="联系方式的备注信息", help_text="联系方式的备注信息，用于助记，不超过30个字符"
    )
    skip_verify = mongoengine.BooleanField(
        verbose_name="外部客户添加时是否无需验证，默认为true",
        default=True,
        help_text="外部客户添加时是否无需验证，默认为true",
    )

    user = mongoengine.ListField(
        mongoengine.StringField(),
        verbose_name="使用该联系方式的用户userID列表",
        help_text="使用该联系方式的用户userID列表，在type为1时为必填，且只能有一个",
    )
    party = mongoengine.ListField(
        mongoengine.StringField(),
        verbose_name="使用该联系方式的部门id列表",
        help_text="使用该联系方式的部门id列表，只在type为2时有效",
    )
    is_temp = mongoengine.BooleanField(
        verbose_name="是否临时会话模式",
        help_text="是否临时会话模式，true表示使用临时会话模式，默认为false",
        default=False,
    )
    expires_in = mongoengine.IntField(
        verbose_name="临时会话二维码有效期(单位秒)",
        help_text="临时会话二维码有效期，以秒为单位。该参数仅在is_temp为true时有效，默认7天",
    )
    chat_expires_in = mongoengine.IntField(
        verbose_name="临时会话有效期(单位秒)",
        help_text="临时会话有效期，以秒为单位。该参数仅在is_temp为true时有效，默认为添加好友后24小时",
    )
    unionid = mongoengine.StringField(
        verbose_name="可进行临时会话的客户unionid",
        help_text="可进行临时会话的客户unionid，该参数仅在is_temp为true时有效，如不指定则不进行限制",
    )
    conclusions = mongoengine.DictField(
        verbose_name="结束语", help_text="结束语，会话结束时自动发送给客户，可参考“结束语定义”，仅在is_temp为true时有效"
    )
    qr_code = mongoengine.StringField(
        verbose_name="联系我二维码链接",
        help_text="联系我二维码链接，仅在scene为2时返回",
    )

    def __str__(self):
        return self.state

    meta = {
        "collection": "wecom_contact_way",
        "indexes": [
            "#state",
            "#type",
            "#scene",
        ],
        "abstract": True,
    }

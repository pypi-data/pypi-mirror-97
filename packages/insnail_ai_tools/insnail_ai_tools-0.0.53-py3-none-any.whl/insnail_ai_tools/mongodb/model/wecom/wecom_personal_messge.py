import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin
from insnail_ai_tools.mongodb.model.wecom.meta import WecomMessageActionChoices


class WecomPersonalMessage(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    origin data scheme:
    +--------------+-------------+------+-----+---------+-------+
    | Field        | Type        | Null | Key | Default | Extra |
    +--------------+-------------+------+-----+---------+-------+
    | msg_id       | varchar(64) | NO   | MUL | NULL    |       |
    | action       | varchar(10) | YES  |     | NULL    |       |
    | msg_type     | varchar(32) | NO   |     | NULL    |       |
    | from_user_id | varchar(64) | NO   |     | NULL    |       |
    | to_user_id   | varchar(64) | NO   |     | NULL    |       |
    | msg_time     | timestamp   | YES  |     | NULL    |       |
    | unionid      | varchar(64) | NO   | MUL | NULL    |       |
    | content      | text        | YES  |     | NULL    |       |
    | url          | text        | YES  |     | NULL    |       |
    | create_time  | timestamp   | YES  |     | NULL    |       |
    +--------------+-------------+------+-----+---------+-------+
    """

    msg_id = mongoengine.StringField(
        verbose_name="消息id",
        primary_key=True,
        help_text="消息id，消息的唯一标识，企业可以使用此字段进行消息去重。msg_id以_external结尾的消息，表明该消息是一条外部消息。",
    )
    action = mongoengine.StringField(
        verbose_name="action",
        max_length=16,
        choices=WecomMessageActionChoices.choices(),
        default="send",
        required=True,
    )
    # 消息格式，参考 https://work.weixin.qq.com/api/doc/90000/90135/91774#消息格式
    msg_type = mongoengine.StringField(verbose_name="消息类型", max_length=64)

    # 身份识别相关
    from_user_id = mongoengine.StringField(
        verbose_name="发送者id",
        max_length=64,
        help_text="同一企业内容为userid，非相同企业为external_userid。消息如果是机器人发出，也为external_userid。String类型",
    )
    to_user_id = mongoengine.StringField(
        verbose_name="接收人id",
        max_length=64,
        help_text="同一企业内容为userid，非相同企业为external_userid。消息如果是机器人发出，也为external_userid。String类型",
    )
    unionid = mongoengine.StringField(
        verbose_name="unionid",
        max_length=64,
    )

    # 消息主体内容相关
    content = mongoengine.DictField(verbose_name="消息内容")
    content_text = mongoengine.StringField(
        verbose_name="文本内容", help_text="从content中提取的文本内容，比如图片、语音、文件等会从中提取内容"
    )
    url = mongoengine.StringField(verbose_name="消息附加链接")

    # 时间相关
    msg_time = mongoengine.DateTimeField(verbose_name="消息发送时间戳")
    create_time = mongoengine.DateTimeField(verbose_name="创建时间")

    meta = {
        "collection": "wecom_personal_message",
        "indexes": ["#msg_id", "#msg_type", "msg_time", "create_time"],
        "abstract": True,
    }

    def __str__(self):
        return self.msg_id

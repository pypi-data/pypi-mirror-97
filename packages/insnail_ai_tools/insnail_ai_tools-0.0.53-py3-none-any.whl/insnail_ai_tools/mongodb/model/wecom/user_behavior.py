import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class WecomUserBehavior(mongoengine.DynamicDocument, MultiDatabaseMixin):
    user_id = mongoengine.StringField(verbose_name="对应的user", help_text="对应的user")
    stat_time = mongoengine.DateField(verbose_name="数据日期", help_text="数据日期，为当日0点")

    # 人
    new_apply_cnt = mongoengine.IntField(
        verbose_name="发起申请数",
        help_text="发起申请数，"
        "成员通过「搜索手机号」、「扫一扫」、"
        "「从微信好友中添加」、「从群聊中添加」、"
        "「添加共享、分配给我的客户」、「添加单向、双向删除好友关系的好友」、"
        "「从新的联系人推荐中添加」等渠道主动向客户发起的好友申请数量。",
        default=0,
    )
    new_contact_cnt = mongoengine.IntField(
        verbose_name="新增客户数", help_text="新增客户数，成员新添加的客户数量。", default=0
    )
    chat_cnt = mongoengine.IntField(
        verbose_name="聊天总数", help_text="聊天总数， 成员有主动发送过消息的单聊总数。", default=0
    )
    message_cnt = mongoengine.IntField(
        verbose_name="发送消息数", help_text="发送消息数，成员在单聊中发送的消息总数。", default=0
    )
    reply_percentage = mongoengine.FloatField(
        verbose_name="已回复聊天占比",
        help_text="已回复聊天占比，浮点型，客户主动发起聊天后，成员在一个自然日内有回复过消息的聊天数/客户主动发起的聊天数比例，"
        "不包括群聊，仅在确有聊天时返回。",
        default=0,
    )
    avg_reply_time = mongoengine.IntField(
        verbose_name="平均首次回复时长，单位为分钟",
        help_text="平均首次回复时长，单位为分钟，即客户主动发起聊天后，成员在一个自然日内首次回复的时长间隔为首次回复时长，"
        "所有聊天的首次回复总时长/已回复的聊天总数即为平均首次回复时长，不包括群聊，仅在确有聊天时返回。",
        default=0,
    )
    negative_feedback_cnt = mongoengine.IntField(
        verbose_name="删除及拉黑成员的客户数", help_text="删除/拉黑成员的客户数，即将成员删除或加入黑名单的客户数。", default=0
    )

    # 群

    new_chat_cnt = mongoengine.IntField(
        verbose_name="新增客户群数量", help_text="新增客户群数量", default=0
    )
    chat_total = mongoengine.IntField(
        verbose_name="截至当天客户群总数量", help_text="截至当天客户群总数量", default=0
    )
    chat_has_msg = mongoengine.IntField(
        verbose_name="截至当天有发过消息的客户群数量", help_text="截至当天有发过消息的客户群数量", default=0
    )
    new_member_cnt = mongoengine.IntField(
        verbose_name="客户群新增群人数", help_text="客户群新增群人数。", default=0
    )
    member_total = mongoengine.IntField(
        verbose_name="截至当天客户群总人数", help_text="截至当天客户群总人数", default=0
    )
    member_has_msg = mongoengine.IntField(
        verbose_name="截至当天有发过消息的群成员数", help_text="截至当天有发过消息的群成员数", default=0
    )
    msg_total = mongoengine.IntField(
        verbose_name="截至当天客户群消息总数", help_text="截至当天客户群消息总数", default=0
    )

    meta = {
        "collection": "wecom_user_behavior",
        "indexes": ["#userid", "stat_time"],
        "abstract": True,
    }

    def __str__(self):
        return self.user_id

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class WecomUserRelation(mongoengine.DynamicDocument, MultiDatabaseMixin):
    userid = mongoengine.StringField(
        verbose_name="用户ID",
        help_text="添加了外部联系人(客户)的企业成员userid",
        max_length=64,
        reference="wecom_user",
    )
    external_userid = mongoengine.StringField(
        verbose_name="客户ID",
        help_text="企业员工添加的客户userid",
        max_length=64,
        unique_with="userid",
        reference="wecom_external_user",
    )

    remark = mongoengine.StringField(
        verbose_name="企业成员对此外部联系人的备注", help_text="企业成员对此外部联系人的备注"
    )
    description = mongoengine.StringField(
        verbose_name="企业成员对此外部联系人的描述", help_text="企业成员对此外部联系人的描述"
    )
    createtime = mongoengine.DateTimeField(
        verbose_name="企业成员添加此外部联系人的时间", help_text="企业成员添加此外部联系人的时间"
    )
    # tags = mongoengine.EmbeddedDocumentListField(
    #     TagInfo,
    #     verbose_name="企业成员添加此外部联系人所打标签的信息列表",
    #     help_text="企业成员添加此外部联系人所打标签的信息列表",
    # )
    tag_id = mongoengine.ListField(mongoengine.StringField(), verbose_name="标签列表")

    remark_corp_name = mongoengine.StringField(
        verbose_name="企业成员对此客户备注的企业名称", help_text="企业成员对此客户备注的企业名称"
    )
    remark_mobiles = mongoengine.ListField(
        mongoengine.StringField(),
        verbose_name="企业成员对此客户备注的手机号码",
        help_text="企业成员对此客户备注的手机号码，第三方不可获取",
    )
    # 来源定义 https://work.weixin.qq.com/api/doc/90000/90135/92114#%E6%9D%A5%E6%BA%90%E5%AE%9A%E4%B9%89
    add_way = mongoengine.IntField(
        verbose_name="企业成员添加此客户的来源",
        choices=(
            (0, "未知来源"),
            (1, "扫描二维码"),
            (2, "搜索手机号"),
            (3, "名片分享"),
            (4, "群聊"),
            (5, "手机通讯录"),
            (6, "微信联系人"),
            (7, "来自微信的添加好友申请"),
            (8, "安装第三方应用时自动添加的客服人员"),
            (9, "搜索邮箱"),
            (201, "内部成员共享"),
            (202, "管理员/负责人分配"),
        ),
        help_text="企业成员添加此客户的来源",
    )
    oper_userid = mongoengine.StringField(
        verbose_name="发起添加的userid",
        help_text="发起添加的userid，如果成员主动添加，为成员的userid；如果是客户主动添加，则为客户的外部联系人userid；如果是内部成员共享/管理员分配，则为对应的成员/管理员userid",
    )
    state = mongoengine.StringField(
        verbose_name="企业自定义的state参数",
        help_text="企业自定义的state参数，用于区分客户具体是通过哪个「联系我」添加，由企业通过创建「联系我」方式指定",
    )
    is_delete = mongoengine.BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )

    def __str__(self) -> str:
        return f"{self.userid}_{self.external_userid}"

    meta = {
        "collection": "wecom_user_relation",
        "indexes": [
            "#userid",
            "#external_userid",
            "createtime",
            "#add_way",
        ],
        "abstract": True,
    }

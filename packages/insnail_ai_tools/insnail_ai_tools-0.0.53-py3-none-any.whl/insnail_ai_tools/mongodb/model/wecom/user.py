import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin
from insnail_ai_tools.mongodb.model.wecom.meta import WecomUserExternalProfile


class WecomUser(mongoengine.DynamicDocument, MultiDatabaseMixin):
    userid = mongoengine.StringField(
        verbose_name="成员UserID",
        primary_key=True,
        max_length=64,
        help_text="成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节",
    )
    name = mongoengine.StringField(
        verbose_name="成员名称",
        help_text="成员名称；第三方不可获取，调用时返回userid以代替name；对于非第三方创建的成员，第三方通讯录应用也不可获取；第三方页面需要通过通讯录展示组件来展示名字",
        required=True,
    )
    mobile = mongoengine.StringField(
        verbose_name="手机号码", help_text="手机号码，第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    department = mongoengine.ListField(
        mongoengine.IntField(),
        verbose_name="成员所属部门id列表",
        help_text="成员所属部门id列表，仅返回该应用有查看权限的部门id",
    )
    order = mongoengine.ListField(
        mongoengine.IntField(),
        verbose_name="部门内的排序值",
        help_text="部门内的排序值，默认为0。数量必须和department一致，数值越大排序越前面。值范围是[0, 2^32)",
    )

    position = mongoengine.StringField(
        verbose_name="职务信息", help_text="职务信息；第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    gender = mongoengine.StringField(
        verbose_name="性别", help_text="性别。0表示未定义，1表示男性，2表示女性"
    )

    email = mongoengine.StringField(
        verbose_name="邮箱", help_text="邮箱，第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    is_leader_in_dept = mongoengine.ListField(
        mongoengine.IntField(),
        verbose_name="部门内是否为上级",
        help_text="表示在所在的部门内是否为上级。；第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取",
    )

    avatar = mongoengine.StringField(
        verbose_name="头像url", help_text="头像url。 第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    thumb_avatar = mongoengine.StringField(
        verbose_name="头像缩略图url",
        help_text="头像缩略图url。 第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取",
    )
    telephone = mongoengine.StringField(
        verbose_name="座机", help_text="座机。第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    alias = mongoengine.StringField(
        verbose_name="别名", help_text="别名；第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )
    extattr = mongoengine.DictField(
        verbose_name="扩展属性", help_text="扩展属性，第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取"
    )

    status = mongoengine.IntField(
        verbose_name="激活状态",
        help_text="激活状态: 1=已激活，2=已禁用，4=未激活，5=退出企业。已激活代表已激活企业微信或已关注微工作台（原企业号）。未激活代表既未激活企业微信又未关注微工作台（原企业号）。",
    )
    qr_code = mongoengine.StringField(
        verbose_name="员工个人二维码",
        help_text="员工个人二维码，扫描可添加为外部联系人(注意返回的是一个url，可在浏览器上打开该url以展示二维码)；第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取",
    )
    main_department = mongoengine.IntField(verbose_name="主部门", help_text="主部门")
    address = mongoengine.StringField(verbose_name="地址", help_text="地址。长度最大128个字符")

    isleader = mongoengine.IntField(verbose_name="", help_text="")
    enable = mongoengine.IntField(verbose_name="", help_text="")
    hide_mobile = mongoengine.IntField(verbose_name="", help_text="")

    external_profile = mongoengine.EmbeddedDocumentField(
        WecomUserExternalProfile,
        verbose_name="成员对外属性",
        help_text="成员对外属性，字段详情见对外属性；第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取",
    )
    external_position = mongoengine.StringField(
        verbose_name="对外职务",
        help_text="对外职务，如果设置了该值，则以此作为对外展示的职务，否则以position来展示。第三方仅通讯录应用可获取；对于非第三方创建的成员，第三方通讯录应用也不可获取",
    )
    ai_calendar_id = mongoengine.StringField(
        verbose_name="AI助手日历ID", help_text="Ai助手会对每个在职员工创建一个日历，用以帮员工记录日程"
    )
    is_delete = mongoengine.BooleanField(
        verbose_name="是否被删除", help_text="是否被删除，采取软删除", default=False
    )

    meta = {
        "collection": "wecom_user",
        "indexes": [
            "is_delete",
        ],
        "abstract": True,
    }

    def __str__(self):
        return self.name

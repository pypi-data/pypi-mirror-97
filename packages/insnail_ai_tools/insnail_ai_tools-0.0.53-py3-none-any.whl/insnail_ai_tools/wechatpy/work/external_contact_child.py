import time
from typing import List

from optionaldict import optionaldict

try:
    from wechatpy.work.client.api import WeChatExternalContact
except ImportError:
    from wechatpy.enterprise.client.api import WeChatExternalContact


class WeChatExternalContactChild(WeChatExternalContact):
    """
    客户联系人扩展类
    """

    def get_user_behavior_data_v2(
        self,
        userid: List[str] = None,
        partyid: List[int] = None,
        start_time: int = None,
        end_time: int = None,
    ):
        """
        企业可通过此接口获取成员联系客户的数据，包括发起申请数、新增客户数、聊天数、发送消息数和删除/拉黑成员的客户数等指标。
        userid和partyid不可同时为空;
        https://work.weixin.qq.com/api/doc/90000/90135/92132
        :param userid: 成员ID列表，最多100个
        :param partyid: 部门ID列表，最多100个
        :param start_time: 数据起始时间, 当传入的时间不为0点时间戳时，会向下取整，默认为昨天
        :param end_time: 数据结束时间, 当传入的时间不为0点时间戳时，会向下取整， 默认为昨天
        :return: 返回的 JSON 数据包
        """
        assert userid or partyid
        if not start_time:
            start_time = int(time.time()) - 86400
        if not end_time:
            end_time = int(time.time()) - 86400
        data = optionaldict(
            userid=userid,
            partyid=partyid,
            start_time=start_time,
            end_time=end_time,
        )
        return self._post("externalcontact/get_user_behavior_data", data=data)

    def get_external_group_list(
        self, userid_list: list, status_filter: int = 0, limit: int = 100
    ) -> list:
        """
         获取客户群列表
        https://work.weixin.qq.com/api/doc/90000/90135/92120

        :param userid_list: 企业员工userid标识列表
        :param status_filter: 客户群跟进状态过滤。0 - 所有列表(即不过滤), 1 - 离职待继承, 2 - 离职继承中, 3 - 离职继承完成，默认0
        :param limit: 分页，预期请求的数据量，取值范围 limit: 1~ 1000，默认100
        :return: []
        """
        cursor = ""
        group_chat_list = []
        # owner_filter: 群主userid过滤
        #     userid_list: 企业微信员工userid列表
        # cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用不填
        data = optionaldict(
            status_filter=status_filter,
            owner_filter={"userid_list": userid_list},
            cursor=cursor,
            limit=limit,
        )
        try:
            while True:
                response = self._post("externalcontact/groupchat/list", data=data)
                if (response["errcode"] == 0) and response.get("cursor"):
                    data["cursor"] = response.get("cursor")
                    group_chat_list.extend(response.get("group_chat_list"))
                else:
                    break
            return group_chat_list
        except Exception as e:
            print(e)
            return []

    def get_external_group_statistic_data_by_userid(
        self, userid_list: list, start_time: int = None, end_time: int = None
    ) -> list:
        """
         获取userid为群主的「群聊数据统计」数据
        https://work.weixin.qq.com/api/doc/90000/90135/92133

        :param userid_list: 企业员工userid标识列表
        :param start_time: 数据开始时间；开始时间与结束时间只传一个，默认获取传入时间当天的数据，如果两个都没有传，默认获取昨天的数据
        :param end_time: 数据结束时间
        :return: []
        """
        try:
            external_behavior_list = []
            offset = 0
            # owner_filter: 群主userid过滤，如果不填，表示获取全部群主的数据
            #     userid_list: 企业微信员工userid列表，最多100个
            parameter = {"owner_filter": {"userid_list": userid_list}, "offset": offset}
            if start_time and end_time:
                parameter["day_begin_time"] = start_time
                parameter["day_end_time"] = end_time
            elif start_time:
                parameter["day_begin_time"] = start_time
            elif end_time:
                parameter["day_begin_time"] = end_time
            else:
                parameter["day_begin_time"] = time.time() - 86400
            while True:
                response = self._post(
                    "externalcontact/groupchat/statistic", data=parameter
                )
                external_behavior_list.extend(response.get("items"))
                if response.get("total") == response.get("next_offset"):
                    break
                else:
                    parameter["offset"] = response.get("next_offset")
            return external_behavior_list
        except Exception as e:
            print(e)
            return []

    def get_user_behavior_data_by_userid(
        self, userid: str, start_time: int = None, end_time: int = None
    ) -> list:
        """
         获取该userid员工「联系客户统计」数据
        https://work.weixin.qq.com/api/doc/90000/90135/92132

        :param userid: 企业微信userid标识
        :param start_time: 数据开始时间，开始时间与结束时间只传一个，默认获取传入时间当天的数据，如果两个都没有传，默认获取昨天的数据
        :param end_time: 数据结束时间
        :return: []
        """
        try:
            if start_time and end_time:
                parameter_start_time = start_time
                parameter_end_time = end_time
            elif start_time:
                parameter_start_time = start_time
                parameter_end_time = start_time
            elif end_time:
                parameter_start_time = end_time
                parameter_end_time = end_time
            else:
                # 测试时间
                # parameter_start_time = 1609224560
                # parameter_end_time = 1609224560
                yesterday = time.time() - 86400
                parameter_start_time = yesterday
                parameter_end_time = yesterday
            res = self.get_user_behavior_data(
                userid, parameter_start_time, parameter_end_time
            )
            if res.get("errcode") == 0:
                return res.get("behavior_data")
            else:
                return []
        except Exception as e:
            print(e)
            return []

    def batch_get_by_user(self, userid: str, cursor: str = "", limit: int = 50) -> dict:
        """
        批量获取客户详情

        使用示例：

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 批量获取该企业员工添加的客户(外部联系人)的详情
            external_contact_list = client.external_contact.batch_get_by_user("user_id", "cursor", 10)["external_contact_list"]

        :param userid: 企业成员的userid
        :param cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用可不填
        :param limit: 返回的最大记录数，整型，最大值100，默认值50，超过最大值时取最大值
        :return: 包含该企业员工添加的部分客户详情列表的字典类型数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 第三方/自建应用调用此接口时，userid需要在相关应用的可见范围内。

        .. _批量获取客户详情: https://work.weixin.qq.com/api/doc/90000/90135/92994
        """
        data = optionaldict(
            userid=userid,
            cursor=cursor,
            limit=limit,
        )
        return self._post("externalcontact/batch/get_by_user", data=data)

    def get_all_by_user(self, userid: str, limit: int = 50) -> list:
        """
        获取企业员工添加的所有客户详情列表

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            #  获取企业员工添加的所有客户详情列表
            total_external_contact_list = client.external_contact.get_all_by_user("user_id", 10)

        :param userid: 企业员工userid
        :param limit: 返回的最大记录数，整型，最大值100，默认值50，超过最大值时取最大值
        :return: 企业员工添加的所有客户详情列表

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 第三方/自建应用调用此接口时，userid需要在相关应用的可见范围内。
        """
        cursor = ""
        total_external_contact_list = []
        while True:
            response = self.batch_get_by_user(userid, cursor, limit)
            if response.get("errcode") == 0:
                total_external_contact_list.extend(
                    response.get("external_contact_list")
                )
            if not response.get("next_cursor"):
                break
            else:
                cursor = response.get("next_cursor")
        return total_external_contact_list

    def add_contact_way_full(
        self,
        type_: int = 2,
        scene: int = 2,
        style: int = None,
        remark: str = None,
        skip_verify: bool = True,
        state: str = None,
        user_list: List[str] = None,
        department_list: List[str] = None,
        is_temp: bool = False,
        expires_in: int = None,
        chat_expires_in: int = None,
        unionid: str = None,
        conclusions: dict = None,
    ):
        """
        通过API添加的「联系我」不会在管理端进行展示，每个企业可通过API最多配置50万个「联系我」。
        用户需要妥善存储返回的config_id，config_id丢失可能导致用户无法编辑或删除「联系我」。
        临时会话模式不占用「联系我」数量，但每日最多添加10万个，并且仅支持单人。
        临时会话模式的二维码，添加好友完成后该二维码即刻失效。
        https://work.weixin.qq.com/api/doc/90000/90135/92572
        :param type_: 联系方式类型,1-单人, 2-多人
        :param scene: 场景，1-在小程序中联系，2-通过二维码联系
        :param style: 在小程序中联系时使用的控件样式，详见附表 https://work.weixin.qq.com/api/doc/90000/90135/92572#%E9%99%84%E5%BD%95
        :param remark: 联系方式的备注信息，用于助记，不超过30个字符
        :param skip_verify: 外部客户添加时是否无需验证，默认为true
        :param state: 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取外部联系人详情”时会返回该参数值，不超过30个字符
        :param user_list: 使用该联系方式的用户userID列表，在type为1时为必填，且只能有一个
        :param department_list: 使用该联系方式的部门id列表，只在type为2时有效
        :param is_temp: 是否临时会话模式，true表示使用临时会话模式，默认为false
        :param expires_in: 临时会话二维码有效期，以秒为单位。该参数仅在is_temp为true时有效，默认7天
        :param chat_expires_in: 临时会话有效期，以秒为单位。该参数仅在is_temp为true时有效，默认为添加好友后24小时
        :param unionid: 可进行临时会话的客户unionid，该参数仅在is_temp为true时有效，如不指定则不进行限制
        :param conclusions: 结束语，会话结束时自动发送给客户，可参考“结束语定义”，仅在is_temp为true时有效
        :return: 返回的 JSON 数据包
        """
        assert remark and len(remark) > 30, "remark，remark"
        assert state and len(state) > 30, "如果指定state，state不得超过30个字符"
        data = optionaldict(
            type=type_,
            scene=scene,
            style=style,
            remark=remark,
            skip_verify=skip_verify,
            state=state,
            user=user_list,
            party=department_list,
            is_temp=is_temp,
            expires_in=expires_in,
            chat_expires_in=chat_expires_in,
            unionid=unionid,
            conclusions=conclusions,
        )
        return self._post("externalcontact/add_contact_way", data=data)

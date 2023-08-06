import requests


class WeComUserExternalInfo:
    def __init__(self, external_info_url: str):
        self._external_info_url = external_info_url

    def get_user_info_by_token(self, token: str):
        """
            通过token获取成员信息
        Args:
            token:

        Returns:
            example：
                {
                    "code": 0, # 状态码
                    "msg": msg, # 描述语
                    "data": {
                        'external_contact_list': [], # 客户列表
                        'external_group_list': [], # 客户群列表
                        'external_behavior_data': [], # 客户联系客户统计数据
                        'external_group_statistic_data': [], # 群聊数据统计数据
                    }
                }
        """
        # GET_USER_INFO_URL = "http://127.0.0.1:8000/cas/getWeComCustomerInfo"
        data = {"token": token}
        res = requests.get(url=self._external_info_url, params=data)
        return res.json()

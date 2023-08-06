from unittest import mock

from insnail_ai_tools.web.wecom_util import WeComUserExternalInfo


def test_get_user_info_by_token():
    return_success = mock.Mock(return_value={"code": 0, "msg": ""})
    wecom = WeComUserExternalInfo("http://127.0.0.1:8000/cas/getWeComCustomerInfo")
    wecom.get_user_info_by_token = return_success
    token = "rjnx($hyt!w)ie*vgu#dobqk&asmzf"
    res = wecom.get_user_info_by_token(token)
    assert res["code"] == 0

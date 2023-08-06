import inspect

from wechatpy.client import WeChatClient as WeChatClient
from wechatpy.client.base import BaseWeChatClient, _is_api_endpoint
from wechatpy.work.client import WeChatClient as WecomClient

from insnail_ai_tools.wechatpy.work import (
    WeChatDepartmentChild,
    WeChatExternalContactChild,
    WeChatExternalContactGroupChat,
)
from insnail_ai_tools.wechatpy.work.event import *


def inject_client(client_class: BaseWeChatClient):
    """
    对指定client做注入重写的类。此方法只对重写的类生效，更多的子类继承，需调用不同类的inject
    """
    api_endpoints = inspect.getmembers(client_class, _is_api_endpoint)
    for name, api in api_endpoints:
        api_cls = type(api)
        sub_class = api_cls.__subclasses__()
        if sub_class:
            setattr(client_class, name, sub_class[0](client_class))


def inject_wechat_client(wechat_client: WeChatClient):
    """个人微信类的注入"""
    inject_client(wechat_client)


def inject_wecom_client(wecom_client: WecomClient):
    """企业微信类的注入"""

    inject_client(wecom_client)
    setattr(
        wecom_client,
        "external_contact_group_chat",
        WeChatExternalContactGroupChat(wecom_client),
    )

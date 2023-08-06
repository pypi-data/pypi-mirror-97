from typing import List

from httpx import Response

from insnail_ai_tools.httpx import aio_get, aio_post

NEO_ORDER_SYSTEM_PREFIX: str = "http://qasinternal.insnail.com/neo-order-system"
NEO_PRODUCT_SYSTEM_PREFIX: str = "http://internal.insnail.com/neo-product-system"
NEO_DATA_SEARCH_PREFIX: str = "http://internal.insnail.com/neo-data-search"


async def common_response_extract(response: Response):
    if response.status_code == 200:
        result = response.json()
        if result["code"] == "0000":
            return result["data"]


async def get_policy_list(user_id: str) -> list:
    """
    根据user_id 从 neo order system获取用户的订单信息
    :param user_id:
    :return:
    """
    assert NEO_ORDER_SYSTEM_PREFIX, "NEO_ORDER_SYSTEM_PREFIX"
    url = f"{NEO_ORDER_SYSTEM_PREFIX}/app/policy/list/robot"
    response = await aio_get(url, params={"user_id": user_id})
    return await common_response_extract(response)


async def get_policy_detail(policy_id: str) -> dict:
    assert NEO_ORDER_SYSTEM_PREFIX, "NEO_ORDER_SYSTEM_PREFIX"
    url = f"{NEO_ORDER_SYSTEM_PREFIX}/app/policy/detail/policy-code"
    response = await aio_get(url, params={"policy_code": policy_id})
    return await common_response_extract(response)


async def get_policy_can_cancel(policy_id: str, user_id) -> bool:
    assert NEO_ORDER_SYSTEM_PREFIX, "NEO_ORDER_SYSTEM_PREFIX"
    url = f"{NEO_ORDER_SYSTEM_PREFIX}/insurance/policies/brief-info/{policy_id}?userId={user_id}"
    response = await aio_get(url, params={"policy_code": policy_id})
    data = await common_response_extract(response)
    if data:
        return data["surrenderable"]
    else:
        return False


async def get_insurance_company_info_by_name(name: str) -> dict:
    # 通过公司名获取公司的信息
    # customerTel 客服电话
    assert NEO_PRODUCT_SYSTEM_PREFIX, "NEO_PRODUCT_SYSTEM_PREFIX"
    url = f"{NEO_PRODUCT_SYSTEM_PREFIX}/base-config/query/company"
    data = {"pageNum": 0, "pageSize": 100, "condition": {"name": name}}
    response = await aio_post(url, json=data)
    data = await common_response_extract(response)
    if data:
        return data[0]


async def get_insurance_company_list() -> list:
    """从neo获取公司列表"""
    assert NEO_PRODUCT_SYSTEM_PREFIX, "NEO_PRODUCT_SYSTEM_PREFIX"
    url = f"{NEO_PRODUCT_SYSTEM_PREFIX}/base/company"
    response = await aio_get(url)
    return await common_response_extract(response)


async def get_insurance_product_list_from_insurance_center() -> list:
    """从保险大全获取产品列表"""
    assert NEO_PRODUCT_SYSTEM_PREFIX, "NEO_PRODUCT_SYSTEM_PREFIX"
    url = f"{NEO_PRODUCT_SYSTEM_PREFIX}/collection/display/query-internal"
    response = await aio_get(url)
    return await common_response_extract(response)


async def get_product_detail_from_insurance_center(name: str) -> dict:
    """从保险大全获取产品信息"""
    assert NEO_PRODUCT_SYSTEM_PREFIX, "NEO_PRODUCT_SYSTEM_PREFIX"
    url = (
        f"{NEO_PRODUCT_SYSTEM_PREFIX}/collection/display/query/detail?goodsName={name}"
    )
    response = await aio_get(url)
    return await common_response_extract(response)


async def search_product_by_neo_data_search(
    product_name: str, offset: int = 0, limit: int = 10
) -> List[dict]:
    """搜索保险产品"""
    assert NEO_DATA_SEARCH_PREFIX, "NEO_DATA_SEARCH_PREFIX"
    url = f"{NEO_DATA_SEARCH_PREFIX}/search/common"
    data = {"input": product_name, "type": "product", "from": offset, "size": limit}
    response = await aio_post(url, json=data)
    return await common_response_extract(response)


async def get_insurance_health_notification(goods_code: str) -> List[dict]:
    assert NEO_PRODUCT_SYSTEM_PREFIX, "NEO_PRODUCT_SYSTEM_PREFIX"
    url = f"{NEO_PRODUCT_SYSTEM_PREFIX}/goods/info/ark"
    data = {
        "pageNum": 0,
        "pageSize": 1,
        "compress": False,
        "condition": {"goodsCodeList": [goods_code]},
    }
    response = await aio_post(url, json=data)
    result = await common_response_extract(response)
    return result[0]["healthNotificationList"]

import pytest

from insnail_ai_tools.ark_api import (
    get_insurance_company_list,
    get_insurance_product_list_from_insurance_center,
    get_product_detail_from_insurance_center,
    search_product_by_neo_data_search,
)


@pytest.mark.asyncio
async def test_get_insurance_company_list():
    data = await get_insurance_company_list()
    print(data)


@pytest.mark.asyncio
async def test_get_insurance_product_list_from_insurance_center():
    data = await get_insurance_product_list_from_insurance_center()
    print(data)


@pytest.mark.asyncio
async def test_get_product_detail_from_insurance_center():
    data = await get_product_detail_from_insurance_center("永乐A款重大疾病保险")
    print(data)


@pytest.mark.asyncio
async def test_search_product_by_neo_data_search():
    data = await search_product_by_neo_data_search("永乐a")
    print(data)

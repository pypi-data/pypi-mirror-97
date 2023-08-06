from dataclasses import dataclass

import pytest

from insnail_ai_tools.mdb import MdbDataMixin, MdbInsertUtil

mdb_insert_util = MdbInsertUtil("http://172.18.23.31:8002")


@dataclass
class MdbTestData(MdbDataMixin):
    str1: str
    str2: str
    int1: int
    int2: int


test_table = "table_test"
test_data = MdbTestData(str1="abc", str2="", int1=10, int2=0).as_dict()


def test_report_batch_data():
    result = mdb_insert_util.report_batch_data("table_test", [test_data])
    assert result["msg"] == "success"


@pytest.mark.asyncio
async def test_report_batch_data_async():
    result = await mdb_insert_util.report_batch_data_async("table_test", [test_data])
    assert result["msg"] == "success"

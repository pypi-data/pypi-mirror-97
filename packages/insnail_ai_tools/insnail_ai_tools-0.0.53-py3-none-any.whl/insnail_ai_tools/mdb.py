import logging
from dataclasses import asdict
from typing import List
from urllib.parse import urljoin

import aiohttp
import requests


class MdbInsertUtil:
    """
    example:
    >>> mdb_insert_util = MdbInsertUtil(base_url="")
    >>> mdb_insert_util.report_batch_data("test_table", [])
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.batch_report_url = urljoin(self.base_url, "batch_report_data")

    def report_batch_data(
        self, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        """
        批量上报数据
        :param table: 表名
        :param data_list: 数据， list of dict
        :param mode:
        :return:
        """
        body = self._get_report_body(table, data_list, mode)
        rp = requests.post(self.batch_report_url, json=body)
        result = rp.json()
        logging.info(f"post data to mdb, status [{result['msg']}]")
        return result

    async def report_batch_data_async(
        self, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        """
        批量上报数据， 异步
        :param table: 表名
        :param data_list: 数据， list of dict
        :param mode:
        :return:
        """
        body = self._get_report_body(table, data_list, mode)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.batch_report_url, json=body) as response:
                result = await response.json()
                logging.info(f"post data to mdb, status [{result['msg']}]")
                return result

    @classmethod
    def _get_report_body(
        cls, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        _data_list = []
        for data in data_list:
            d = dict()
            for k, v in data.items():
                if v is not None:
                    d[k] = v
            _data_list.append(d)
        body = {"table": table, "data_list": _data_list}
        if mode:
            body["mode"] = mode
        return body


class MdbDataMixin:
    """Example:
    >>> from dataclasses import dataclass
    >>> @dataclass
    >>> class MdbTestData(MdbDataMixin):
    >>>     f1: str
    >>>     f2: int
    >>> mdb_test_data = MdbTestData(f1="a", f2=1)
    >>> mdb_insert_util = MdbInsertUtil(base_url="")
    >>> mdb_insert_util.report_batch_data("test_table", [mdb_test_data.as_dict()])
    """

    def validate(self):
        """验证数据类型，对不符合的做强制转换"""
        errors = []
        for k, v in self.__dataclass_fields__.items():
            value = getattr(self, k)
            if not isinstance(value, v.type):
                try:
                    value = v.type(value)
                    setattr(self, k, value)
                except ValueError:
                    errors.append(
                        f"参数{k} 期望类型 {v.type}，但是得到类型{type(value)}, 值为[{value}]"
                    )
        if errors:
            raise ValueError(errors)

    def as_dict(self):
        self.validate()
        return asdict(self)

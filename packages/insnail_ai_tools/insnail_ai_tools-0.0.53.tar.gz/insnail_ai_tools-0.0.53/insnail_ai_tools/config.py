import logging
import os
import typing
from typing import Any

import yaml
from pyapollo.apollo_client import ApolloClient


class ConfigBase:
    def _get_config_field(self, field: str) -> Any:
        # 获取field指
        raise NotImplementedError

    def _get_field_type(self, field: str):
        # 获取field的类型
        if field in self.__annotations__:
            return self.__annotations__[field]

    @classmethod
    def _parse_field_type(cls, _type, value):
        try:
            func = getattr(cls, f"_parse_{_type.__name__}", cls._parse_str)
            return func(value)
        except AttributeError:
            func = getattr(cls, f"_parse_{_type.__origin__}", cls._parse_list)
            return func(_type, value)

    @staticmethod
    def _parse_bool(value: str) -> bool:
        return value.lower() not in frozenset(("0", "", "false"))

    @staticmethod
    def _parse_str(value) -> str:
        return str(value)

    @staticmethod
    def _parse_int(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return 0

    @staticmethod
    def _parse_float(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            return 0

    @staticmethod
    def _parse_list(_type, value: str) -> list:
        value = value.split(",")
        result = list()
        for v in value:
            for t in _type.__args__:
                try:
                    result.append(t(v))
                    break
                except ValueError:
                    continue
        return result

    def fetch(self):
        for field in self.__annotations__.keys():
            setattr(self, field, self._get_config_field(field))


class YamlConfig(ConfigBase):
    def __init__(self, yaml_path):
        if os.path.exists(yaml_path):
            with open(yaml_path) as fin:
                self.config_dict = yaml.load(fin.read(), Loader=yaml.FullLoader)
        else:
            self.config_dict = dict()
            print(f"{yaml_path} 不存在")

    def _get_config_field(self, field: str):
        if field in self.config_dict:
            return self.config_dict[field]
        else:
            return getattr(self, field)


class ApolloConfig(ConfigBase):
    def __init__(self, app_id: str, server_url: str, cluster: str = "default"):
        logging.info(
            f"init config object [ApolloConfig], app_id: [{app_id}], server_url: [{server_url}], cluster: [{cluster}]"
        )
        self.apollo_client = ApolloClient(
            app_id=app_id, config_server_url=server_url, cluster=cluster
        )

    def _get_config_field(self, field: str):
        value = self.apollo_client.get_value(field)
        if value is None:
            return getattr(self, field)
        return self._parse_field_type(self._get_field_type(field), value)

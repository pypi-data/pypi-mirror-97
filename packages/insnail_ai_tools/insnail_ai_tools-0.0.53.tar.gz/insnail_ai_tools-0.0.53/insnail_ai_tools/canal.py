import time
from dataclasses import dataclass
from types import FunctionType
from typing import Union

from canal.client import Client
from canal.protocol.EntryProtocol_pb2 import (
    EntryType,
    EventType,
    Header,
    RowChange,
    RowData,
)


@dataclass
class InsertRowData:
    database: str
    table: str
    data: dict


@dataclass
class DeleteRowData:
    database: str
    table: str
    data: dict


@dataclass
class UpdateRowData:
    database: str
    table: str
    before_data: dict
    after_data: dict


class CanalServer:
    def __init__(
        self,
        host: str = "",
        port: str = "",
        username: str = "",
        password: str = "",
        client_id: str = "",
        destination: str = "",
        filters: str = "",
        batch_size: int = 100,
        insert_callback: FunctionType = None,
        update_callback: FunctionType = None,
        delete_callback: FunctionType = None,
    ):
        """
        实例化一个canal 同步的服务
        :param host: canal host
        :param port: canal port
        :param username: canal 用户名
        :param password: canal 密码
        :param client_id: canal client id, ex: 1001
        :param destination: canal destination, ex: example
        :param filters: canal filter, 英文逗号分隔, ex: enterprise.t_enterprise_chat_content
        :param batch_size: 单次轮询处理条数
        :param insert_callback: 插入的callback, 参数为 database, table, row
        :param update_callback: 更新的callback, 参数为 database, table, row
        :param delete_callback: 删除的callback, 参数为 database, table, row
        """
        self.client = Client()
        self.client.connect(host=host, port=port)
        self.client.check_valid(username=username.encode(), password=password.encode())
        self.client.subscribe(
            client_id.encode(), destination.encode(), filters.encode()
        )
        self.batch_size = batch_size
        self.insert_callback = insert_callback
        self.update_callback = update_callback
        self.delete_callback = delete_callback

    async def listen(self):
        while True:
            message = self.client.get(self.batch_size)
            for entry in message["entries"]:
                if entry.entryType in [
                    EntryType.TRANSACTIONBEGIN,
                    EntryType.TRANSACTIONEND,
                ]:
                    continue
                row_change = RowChange()
                row_change.MergeFromString(entry.storeValue)
                for row in row_change.rowDatas:
                    await self.deal_single_row(row_change.eventType, row, entry.header)
            time.sleep(1)

    @classmethod
    async def extract_row_data(
        cls, event_type: EventType, row: RowData, header: Header
    ) -> Union[UpdateRowData, InsertRowData, DeleteRowData]:
        # 删除
        if event_type == EventType.DELETE:
            format_data = dict()
            for column in row.beforeColumns:
                format_data[column.name] = column.value
            else:
                row_data = DeleteRowData(
                    database=header.schemaName, table=header.tableName, data=format_data
                )
        # 插入
        elif event_type == EventType.INSERT:
            format_data = dict()
            for column in row.afterColumns:
                format_data[column.name] = column.value
            else:
                row_data = InsertRowData(
                    database=header.schemaName, table=header.tableName, data=format_data
                )
        # 更新
        else:
            before_data = after_data = dict()
            for column in row.beforeColumns:
                before_data[column.name] = column.value
            for column in row.afterColumns:
                after_data[column.name] = column.value
            row_data = UpdateRowData(
                database=header.schemaName,
                table=header.tableName,
                before_data=before_data,
                after_data=after_data,
            )
        return row_data

    async def deal_single_row(
        self, event_type: EventType, row: RowData, header: Header
    ):
        """
        对canal同步过来的每行做处理
        :param event_type: 事件类型
        :param row: 每行的内容
        :param header: header
        :return:
        """
        row_data = await self.extract_row_data(event_type, row, header)
        # 删除
        if event_type == EventType.DELETE:
            await self.delete_callback(row_data)
        # 插入
        elif event_type == EventType.INSERT:
            await self.insert_callback(row_data)
        # 更新
        else:
            await self.update_callback(row_data)

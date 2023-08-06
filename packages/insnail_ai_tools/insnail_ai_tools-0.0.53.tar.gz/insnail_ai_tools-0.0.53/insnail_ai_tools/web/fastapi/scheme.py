from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    # 基础的response对象，和广州的接口返回格式兼容
    code: str = "0000"
    msg: str = "success"
    data: Any


class BaseDictResponse(BaseResponse):
    # 继承基础的response对象，返回的data是dict类型
    data: Optional[dict] = None


class BaseListResponse(BaseResponse):
    # 继承基础的response对象，返回的data是list类型
    data: Optional[list] = None

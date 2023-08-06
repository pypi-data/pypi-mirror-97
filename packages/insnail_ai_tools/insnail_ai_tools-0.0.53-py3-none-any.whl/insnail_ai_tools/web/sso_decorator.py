# from __future__ import absolute_import
import inspect
from functools import wraps

import redis
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from insnail_ai_tools.web.django.response import BaseResponse as DjangoBaseResponse
from insnail_ai_tools.web.fastapi.scheme import BaseResponse


class Sso:
    def __init__(
        self,
        redis_url: str,
        redis_token_key: str = "login_token",
        header_token_key: str = "authorization",
    ):
        # Config = {"host": "localhost", "port": 6379, "decode_responses": True}
        # pool = redis.ConnectionPool(
        #     host=redis_host,
        #     port=redis_port,
        #     decode_responses=redis_decode_responses,
        # )
        pool = redis.ConnectionPool.from_url(redis_url)
        self._rd = redis.Redis(connection_pool=pool)
        self._redis_token_key = redis_token_key
        self._header_token_key = header_token_key

    def fast_api_sso(self, func):
        """
            fast_api 单点登录拦截装饰器
        Args:
            func:

        Returns:

        """

        @wraps(func)
        def fast_api(*args, **kwargs):
            """
                fast_api的装饰器
            Returns:

            """
            token = kwargs.get(self._header_token_key)
            if token and self._rd.sismember(self._redis_token_key, token):
                pass
            else:
                content = BaseResponse()
                content.code = status.HTTP_401_UNAUTHORIZED
                content.msg = "未登录"
                # 返回失败
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content=jsonable_encoder(content),
                )
                # pass
            return func(*args, **kwargs)

        @wraps(func)
        async def fast_api_async(*args, **kwargs):
            """
                fast_api的装饰器, 异步
            Returns:

            """
            token = kwargs.get(self._header_token_key)
            if token and self._rd.sismember(self._redis_token_key, token):
                pass
            else:
                content = BaseResponse()
                content.code = status.HTTP_401_UNAUTHORIZED
                content.msg = "未登录"
                # 返回失败
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content=jsonable_encoder(content),
                )
                # pass
            res = await func(*args, **kwargs)
            return res

        if inspect.iscoroutinefunction(func):
            return fast_api_async
        else:
            return fast_api

    # def django_sso(self, func):
    #     """
    #         django 单点登录装饰器
    #     Args:
    #         func:
    #
    #     Returns:
    #
    #     """
    #     from django.http import JsonResponse
    #
    #     @wraps(func)
    #     def django(request):
    #         """
    #             django的装饰器
    #         Args:
    #             request:
    #
    #         Returns:
    #
    #         """
    #         token = request.META.get("HTTP_" + self._header_token_key.upper())
    #         if token and self._rd.sismember(self._redis_token_key, token):
    #             pass
    #         else:
    #             # 返回失败
    #             content = DjangoBaseResponse.get_failure("未登录")
    #             content["code"] = (status.HTTP_401_UNAUTHORIZED,)
    #             return JsonResponse(content)
    #         return func(request)
    #
    #     return django

    def register_middleware(self, app_):
        """
            注册app中间件
        Args:
            app_:

        Returns:

        """
        app_.middleware("http")(self._add_process_time_header)

    async def _add_process_time_header(self, request: Request, call_next):
        """
            拦截登录的中间件
        Args:
            request:
            call_next:

        Returns:

        """
        token = request.headers.get(self._header_token_key)
        # print(token)
        if token and self._rd.sismember(self._redis_token_key, token):
            pass
        else:
            content = BaseResponse()
            content.code = (status.HTTP_401_UNAUTHORIZED,)
            content.msg = "未登录"
            # 返回失败
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=jsonable_encoder(content),
            )
        response = await call_next(request)
        return response

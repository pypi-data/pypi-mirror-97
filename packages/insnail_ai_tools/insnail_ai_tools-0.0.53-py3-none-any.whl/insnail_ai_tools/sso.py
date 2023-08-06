import datetime
import inspect
import time
from functools import wraps

import redis
from fastapi import status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt


class Sso:
    def __init__(
        self,
        secret_key: str,
        redis_uri: str,
        redis_key: str = "token",
        expire_minutes: int = 60 * 24,
        algorithm: str = "HS256",
    ):
        self._secret_key = secret_key
        self._expire_minutes = expire_minutes
        self._algorithm = algorithm
        self._redis = redis.Redis.from_url(redis_uri)
        self._redis_key = redis_key

    def generate_token(self, user_id: str) -> str:
        """
        根据用户ID生成token
        :param user_id: 用户ID
        :return: token
        """
        data = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=self._expire_minutes),
        }
        token = jwt.encode(data, self._secret_key, algorithm=self._algorithm)
        return token

    def decode_token(self, token: str) -> dict:
        """
        解码token
        :param token: 对应的token
        :return: 解码结果。exp 为过期时间
        """
        data = jwt.decode(token, self._secret_key)
        return data

    def check_expire(self, token: str) -> bool:
        """
        判断token是否过期
        :param token: 对应token
        :return: True为正常、False为过期
        """
        try:
            data = self.decode_token(token)
        except JWTError:
            return False
        if data["exp"] > time.time():
            return True
        else:
            return False

    def token_to_user_id(self, token: str) -> str:
        return self.decode_token(token)["user_id"]

    def _add_token(self, token: str, user_id: str):
        """
        将token添加至redis。使用hash map， key为用户id， 值为token
        如果redis报错 ResponseError，则有可能是 该KEY的类型为其他类型，需要换个KEY或者将其先清理掉
        :param token: token
        :param user_id: 用户的id
        :return:
        """
        self._redis.hset(self._redis_key, user_id, token)

    def _remove_token(self, token: str):
        """
        移除token，在redis的hash map 中删除该值
        :param token: token
        :return:
        """
        user_id = self.token_to_user_id(token)
        self._redis.hdel(self._redis_key, user_id)

    def _exists_token(self, token: str) -> bool:
        """
        判断token是否在redis中。
        :param token: token
        :return:
        """
        try:
            user_id = self.token_to_user_id(token)
            # 该token 与对应user id 在redis中存在的token是否一致
            return token.encode() == self._redis.hget(self._redis_key, user_id)
        except JWTError:
            return False

    def fast_api_sso(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = kwargs.get("token")
            # token存在且未过期未过期
            try:
                if self._exists_token(token) and self.check_expire(token):
                    return func(*args, **kwargs)
                else:
                    return JSONResponse(
                        {"msg": "token不存在或已过期"},
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
            except Exception as e:
                return JSONResponse(
                    {"msg": "无效的token:{}, error_msg:{}".format(token, e)},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            token = kwargs.get("token")
            # token存在且未过期未过期
            try:
                if self._exists_token(token) and self.check_expire(token):
                    return await func(*args, **kwargs)
                else:
                    return JSONResponse(
                        {"msg": "token不存在或已过期"},
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
            except Exception as e:
                return JSONResponse(
                    {"msg": "无效的token:{}, error_msg:{}".format(token, e)},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    def login(self, user_id: str) -> str:
        """
        通过user_id登录

        :param user_id: 企业微信user_id
        :return: 有效的token
        """
        # 判断该user_id 对应的token是否在redis中，如果存在，判断token是否过期，如果没有过期直接返回
        # 如果过期重新生成token存储redis中并返回
        token = self._redis.hget(self._redis_key, user_id)
        token = token.decode() if token else None
        if token and self.check_expire(token):
            return token
        token = self.generate_token(user_id)
        self._add_token(token, user_id)
        return token

    def logout(self, token: str):
        self._remove_token(token)

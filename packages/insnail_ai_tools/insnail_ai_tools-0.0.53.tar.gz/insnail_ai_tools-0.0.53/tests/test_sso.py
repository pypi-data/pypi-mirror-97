from fastapi.testclient import TestClient
from jose import JWTError
from mockredis.redis import mock_redis_client

from insnail_ai_tools.sso import Sso
from insnail_ai_tools.web import create_fast_api_app

sso = Sso(
    "sso",
    "localhost",
)
sso._redis = mock_redis_client()

app = create_fast_api_app()
client = TestClient(app)

USER_ID = "liqiongyu"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibGlxaW9uZ3l1IiwiZXhwIjoxNjEyMzI0MjY3fQ.ayiqGGAgV19g-fMeAMHOK3SFa07WOZupccyjZrg0whY"


def test_generate_token():
    ex_token_1, ex_token_2, ex_token_3 = TOKEN.split(".")
    token = sso.generate_token(USER_ID)
    token_1, token_2, token_3 = token.split(".")
    assert ex_token_1 == token_1
    assert ex_token_2[:10] == token_2[:10]
    assert ex_token_3 != token_3


def test_decode_token_success():
    data = sso.decode_token(token=TOKEN)
    assert data["user_id"] == USER_ID


def test_decode_token_error():
    try:
        sso.decode_token(token=TOKEN[:-1])
    except Exception as e:
        assert isinstance(e, JWTError)


def test_check_expire():
    assert not sso.check_expire(token=TOKEN[:-1])


def test_token_to_user_id():
    assert USER_ID == sso.token_to_user_id(TOKEN)


def test_redis_token_operate():
    sso._add_token(TOKEN, USER_ID)
    assert sso._redis.hget(sso._redis_key, USER_ID) == TOKEN

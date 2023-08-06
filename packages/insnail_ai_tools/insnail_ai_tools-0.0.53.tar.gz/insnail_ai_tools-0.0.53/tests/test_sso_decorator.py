import time
from unittest import mock

from fastapi import Header
from fastapi.testclient import TestClient

from insnail_ai_tools.web import create_fast_api_app
from insnail_ai_tools.web.sso_decorator import Sso

sso = Sso("redis://@localhost:6379/1")

app = create_fast_api_app()


@app.get("/fun1")
@sso.fast_api_sso
def func1(authorization: str = Header(None)):
    time.sleep(1)
    return {"msg": "success"}


@app.get("/fun2")
def fun2(authorization: str = Header(None)):
    time.sleep(1)
    return {"msg": "success"}


def test_fast_api_sso():
    client = TestClient(app)
    sso._rd.sismember = mock.Mock(return_value=True)
    response = client.get("/fun1", headers={"authorization": "abc"})
    assert response.json() == {"msg": "success"}
    sso._rd.sismember = mock.Mock(return_value=False)
    response = client.get("/fun1", headers={"authorization": "def"})
    assert response.status_code == 401


def test_register_middleware():
    sso.register_middleware(app)
    client = TestClient(app)
    sso._rd.sismember = mock.Mock(return_value=True)
    response = client.get("/fun2", headers={"authorization": "abc"})
    assert response.json() == {"msg": "success"}
    sso._rd.sismember = mock.Mock(return_value=False)
    response = client.get("/fun2", headers={"authorization": "def"})
    assert response.status_code == 401

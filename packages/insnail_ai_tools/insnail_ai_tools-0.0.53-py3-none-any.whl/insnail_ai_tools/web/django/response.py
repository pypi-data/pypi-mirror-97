class BaseResponse:
    @staticmethod
    def get_success(msg="success", data=None):
        response = {"code": 0, "msg": msg, "data": data}
        return response

    @staticmethod
    def get_failure(msg="fail", data=None):
        response = {"code": -1, "msg": msg, "data": data}
        return response

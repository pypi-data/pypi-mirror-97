from wechatpy.messages import BaseMessage


def message_to_dict(msg: BaseMessage) -> dict:
    result = dict()
    for k, v in msg._fields.items():
        result[k] = getattr(msg, k)
    return result

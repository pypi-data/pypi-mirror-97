import pytest

from insnail_ai_tools.email import EmailMessageUtil, EmailServer

# EMAIL
DEFAULT_FROM_EMAIL: str = "algo@ingbaobei.com"

email_server = EmailServer()


def test_send_text():
    msg = EmailMessageUtil("测试发送邮件", DEFAULT_FROM_EMAIL, ["libiao@ingbaobei.com"])
    msg.add_content("一个测试的内容")
    email_server.send_email(msg.msg, ["libiao@ingbaobei.com"])

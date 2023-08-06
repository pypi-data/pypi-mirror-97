import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailMessageUtil:
    def __init__(self, subject: str, from_email: str, to_email_list: list):
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ";".join(to_email_list)
        self.msg = msg

    def add_content(self, content: str, type_: str = "text"):
        """给邮件对象添加正文内容"""
        if type_ == "txt":
            text = MIMEText(content, "plain", "utf-8")
            self.msg.attach(text)

        elif type_ == "html":
            text = MIMEText(content, "html", "utf-8")
            self.msg.attach(text)

    def add_file(self, file_path: str, file_name: str = None):
        """
        给邮件对象添加附件
        :param file_path: 文件路径
        :param file_name: 文件名
        :return: None
        """
        # 构造附件1，传送当前目录下的 test.txt 文件
        with open(file_path, "rb") as fp:
            email_file = MIMEText(fp.read(), "base64", "utf-8")
        email_file["Content-Type"] = "application/octet-stream"
        # file name默认为文件路径中的名字
        file_name = file_name or os.path.basename(file_path)
        email_file.add_header(
            "Content-Disposition", "attachment", filename=("utf-8", "", file_name)
        )

        self.msg.attach(email_file)


class EmailServer:
    """
    邮件发送对象
    :param account: 账户名
    :param password: 密码
    :param host: 邮件服务地址 默认腾讯企业邮箱
    :param port: 邮件服务端口 默认465
    """

    def __init__(
        self,
        account: str = "algo@ingbaobei.com",
        password: str = "Snail123",
        host: str = "smtp.exmail.qq.com",
        port: int = 465,
    ):
        self.account = account
        self.password = password
        self.host = host
        self.port = port
        self.server = None
        self.login()

    def login(self):
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        self.server.login(self.account, self.password)

    def send_email(self, msg: MIMEMultipart = None, to_list: list = None):
        if isinstance(msg, EmailMessageUtil):
            msg = msg.msg

        self.login()
        if to_list:
            for address in to_list:
                self.server.send_message(msg, msg["From"], address)
        else:
            for address in msg["To"].split(";"):
                self.server.send_message(msg, msg["From"], address)

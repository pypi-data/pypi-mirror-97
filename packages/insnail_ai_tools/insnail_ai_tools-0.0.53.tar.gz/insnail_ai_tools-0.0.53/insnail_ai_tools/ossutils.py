import fire
import oss2

ENDPOINT = "https://oss-cn-shenzhen.aliyuncs.com"
ACCESS_KEY_ID = "LTAI4FtSM2t8UaGZSt5bczn8"
ACCESS_KEY_SECRET = "ZxiGRvHBMky2lXPAUyKXuNThxi4Q14"
BUCKET_NAME = "it-snail-dev"
PREFIX = "jumpserver/"
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def _process_filename(name: str):
    return name.split("/")[-1]


def upload(*files, prefix=""):
    """
    上传文件至oss上，默认路径为 jumpserver。
    :param files: 文件列表， 如果文件名为 aaa/bbb.txt， 会被重命名为 bbb.txt
    :param prefix: 为所有文件增加prefix, 如 prefix="aaa/"，则所有文件会被放到 jumpserver/aaa/文件夹下
    :return:
    """
    prefix = PREFIX + prefix
    if not prefix.endswith("/"):
        prefix += "/"
    for name in files:
        with open(name, "rb") as fin:
            print("file: ", name)
            bucket.put_object(prefix + _process_filename(name), fin)


if __name__ == "__main__":
    fire.Fire()

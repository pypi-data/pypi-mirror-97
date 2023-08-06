import mimetypes
import os
import random

import textract

from insnail_ai_tools.httpx import aio_get, aio_head

ALLOW_FILE_SUF = frozenset(
    (
        "csv",
        "doc",
        "docx",
        "eml",
        "epub",
        "htm",
        "html",
        "json",
        "log",
        "msg",
        "odt",
        "ogg",
        "pdf",
        "psv",
        "rtf",
        "tff",
        "tif",
        "tiff",
        "tsv",
        "txt",
        "xls",
        "xlsx",
    )
)


async def url_file_extractor(url: str) -> str:
    response = await aio_head(url)
    ext = mimetypes.guess_extension(response.headers["Content-Type"]).replace(".", "")
    if ext.lower() not in ALLOW_FILE_SUF:
        return "不支持抽取该文件类型"
    response = await aio_get(url)
    filename = f"/tmp/{random.random()}"
    with open(filename, "wb") as fin:
        fin.write(response.content)
    try:
        content = textract.process(filename, extension=ext).decode()
    except Exception as e:
        content = "解析文件出错"
    finally:
        if os.path.exists(filename):
            os.remove(filename)
    return content

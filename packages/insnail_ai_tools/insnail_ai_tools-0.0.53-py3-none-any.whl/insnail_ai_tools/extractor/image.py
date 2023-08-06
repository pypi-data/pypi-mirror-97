import base64
from io import BytesIO
from typing import Dict

import requests
from PIL import Image
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models as ocr_model
from tencentcloud.ocr.v20181119 import ocr_client
from tencentcloud.tiia.v20190529 import models as tiia_model
from tencentcloud.tiia.v20190529 import tiia_client

from insnail_ai_tools.httpx import aio_head


async def process_image_url(url: str) -> tuple:
    """查看url图片的大小，大于4M则下载下来压缩"""
    rp = await aio_head(url)
    image_size = int(rp.headers["Content-Length"])
    if image_size < 4194304:
        return "url", url
    else:
        mul = 3145728 / image_size
        image = requests.get(url).content
        image = Image.open(BytesIO(image))
        x, y = image.size
        image = image.resize((int(x * mul), int(y * mul)))
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPEG")
        image_base64 = base64.b64encode(image_bytes.getvalue())
        return "base64", str(image_base64, "u8")


class TencentImageExtractor:
    def __init__(
        self,
        secret_id: str,
        secret_key: str,
    ):
        cred = credential.Credential(secret_id, secret_key)

        ocr_http_profile = HttpProfile(endpoint="ocr.tencentcloudapi.com")
        ocr_client_profile = ClientProfile(httpProfile=ocr_http_profile)
        self.ocr_client = ocr_client.OcrClient(cred, "ap-guangzhou", ocr_client_profile)

        tiia_http_profile = HttpProfile(endpoint="tiia.tencentcloudapi.com")
        tiia_client_profile = ClientProfile(httpProfile=tiia_http_profile)
        self.tiia_client = tiia_client.TiiaClient(
            cred, "ap-guangzhou", tiia_client_profile
        )

    async def ocr_id_card_from_url(self, image_url: str = None, image_base64=None):
        req = ocr_model.IDCardOCRRequest()
        if image_url:
            req.ImageUrl = image_url
        if image_base64:
            req.ImageBase64 = image_base64
        resp = self.ocr_client.IDCardOCR(req)
        return resp._serialize(allow_none=True)

    async def detect_image_label(self, image_url: str = None, image_base64=None):
        req = tiia_model.DetectLabelRequest()

        if image_url:
            req.ImageUrl = image_url
        if image_base64:
            req.ImageBase64 = image_base64
        req.Scenes = ["CAMERA", "ALBUM", "WEB", "NEWS"]
        resp = self.tiia_client.DetectLabel(req)
        return resp._serialize(allow_none=True)

    async def ocr_image(self, image_url: str = None, image_base64=None):
        req = ocr_model.GeneralAccurateOCRRequest()
        if image_url:
            req.ImageUrl = image_url
        if image_base64:
            req.ImageBase64 = image_base64
        resp = self.ocr_client.GeneralAccurateOCR(req)
        return resp._serialize(allow_none=True)

    async def detect_image_label_by_url(self, url):
        flag, data = await process_image_url(url)
        if flag == "url":
            return await self.detect_image_label(image_url=data)
        else:
            return await self.detect_image_label(image_base64=data)

    async def ocr_image_by_url(self, url):
        flag, data = await process_image_url(url)
        if flag == "url":
            return await self.ocr_image(image_url=data)
        else:
            return await self.ocr_image(image_base64=data)

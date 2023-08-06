"""
Achilles是一个用来存储和管理模型文件的系统，后台地址为 https://achilles.insnail.com。
"""

import os
import sys

import requests


class ModelFile:
    """
    >>> model = ModelFile("ai-coeus", "nlu_model", "0.0.1")
    >>> model.save_model("/root/data/models/ai-coeus-model.pkl")
    """

    def __init__(self, project_slug: str, model_slug: str, version: str):
        self.project_slug = project_slug
        self.model_slug = model_slug
        self.version = version
        self.server_address = "https://achilles.insnail.com"

    def get_model_url(self) -> str:
        data = {
            "project_slug": self.project_slug,
            "model_slug": self.model_slug,
            "version": self.version,
        }
        rp = requests.post(f"{self.server_address}/warehouse/model_url/", data=data)
        if rp.status_code == 200:
            url = rp.json()["url"]
            return url

    def get_model_content(self) -> bytes:
        url = self.get_model_url()
        content = requests.get(url).content
        return content

    def save_model(self, save_path: str, rewrite: bool = True):
        if rewrite:
            os.remove(save_path)
        if os.path.exists(save_path):
            sys.stdout.write(f"[{save_path}] exists!")
        else:
            r = os.system(f"wget {self.get_model_url()} -O {save_path}")
            if r != 0:
                with open(save_path, "wb") as fin:
                    content = self.get_model_content()
                    fin.write(content)

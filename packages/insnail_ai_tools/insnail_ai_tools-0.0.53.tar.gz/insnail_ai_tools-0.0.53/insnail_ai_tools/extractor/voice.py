from tencentcloud.asr.v20190614 import asr_client, models
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


class TencentAsr:
    def __init__(
        self,
        asr_secret_id: str,
        asr_secret_key: str,
        asr_endpoint: str,
        asr_sigh_method: str,
    ):
        self.cred = credential.Credential(asr_secret_id, asr_secret_key)
        self.http_profile = HttpProfile(endpoint=asr_endpoint)
        self.client_profile = ClientProfile(
            httpProfile=self.http_profile, signMethod=asr_sigh_method
        )
        self.client = asr_client.AsrClient(
            self.cred, "ap-shanghai", self.client_profile
        )

    def get_asr_result(self, url: str, format_: str = "mp3") -> dict:
        """
        获取asr的结果。这个接口只支持60s以内的短语音
        :param url: 可公网访问的录音接口
        :param format_: 语音格式
        :return:
            - RequestId: str
            - WordSize: int
            - AudioDuration: int (ms)
            - Result: str(识别结果)
        """
        req = models.SentenceRecognitionRequest()
        req.ProjectId = 0
        req.SubServiceType = 2
        req.SourceType = 0
        req.UsrAudioKey = "session-123"
        req.EngSerViceType = "16k_zh"
        req.VoiceFormat = format_
        req.Url = url
        resp = self.client.SentenceRecognition(req)
        result = resp._serialize()
        return result

    def get_asr_result_from_data(self, data, format_: str = "mp3") -> dict:
        req = models.SentenceRecognitionRequest()
        req.ProjectId = 0
        req.SubServiceType = 2
        req.SourceType = 1
        req.UsrAudioKey = "session-123"
        req.EngSerViceType = "16k_zh"
        req.VoiceFormat = format_
        req.Data = data
        resp = self.client.SentenceRecognition(req)
        result = resp._serialize()
        return result

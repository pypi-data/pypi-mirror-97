import re
from typing import List

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin

ASR_RESULT_PARSE_REGEX = re.compile(
    r"\[([0-9]+:[0-9.]+),([0-9]+:[0-9.]+),(\d+)\]  (.*)"
)


class WecomMeetingVoiceMeta(mongoengine.DynamicEmbeddedDocument):
    start_time = mongoengine.StringField(verbose_name="开始时间")
    end_time = mongoengine.StringField(verbose_name="开始时间")
    text = mongoengine.StringField(verbose_name="对话内容")
    from_role = mongoengine.StringField(verbose_name="发送人角色")

    def __str__(self):
        return f"[{self.start_time}-{self.end_time}] {self.text}"

    @classmethod
    def parse_asr_single_result(cls, line: str) -> dict:
        if line:
            start_time, end_time, from_role, text = ASR_RESULT_PARSE_REGEX.findall(
                line
            )[0]
            return {
                "start_time": start_time,
                "end_time": end_time,
                "from_role": from_role,
                "text": text,
            }

    @classmethod
    def parse_asr_result(cls, asr_result: str) -> List[dict]:
        result = []
        for line in asr_result.split("\n"):
            line = line.strip()
            if line:
                result.append(cls.parse_asr_single_result(line))
        return result

    @classmethod
    def gen_meta_list_from_asr_result(
        cls, asr_result: str
    ) -> List["WecomMeetingVoiceMeta"]:
        result = cls.parse_asr_result(asr_result)
        return [cls(**i) for i in result]


class WecomMeetingVoice(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    origin data scheme:
    +------------------+-------------+------+-----+-------------------+-------+
    | Field            | Type        | Null | Key | Default           | Extra |
    +------------------+-------------+------+-----+-------------------+-------+
    | msg_id           | varchar(64) | NO   | PRI | NULL              |       |
    | user_id          | varchar(64) | NO   |     | NULL              |       |
    | external_user_id | varchar(64) | NO   |     | NULL              |       |
    | union_id         | varchar(64) | YES  | MUL | NULL              |       |
    | talk_time        | bigint(11)  | YES  |     | 0                 |       |
    | call_type        | tinyint(2)  | NO   |     | NULL              |       |
    | custom_type      | tinyint(2)  | NO   |     | 1                 |       |
    | start_time       | timestamp   | YES  |     | NULL              |       |
    | end_time         | timestamp   | YES  |     | NULL              |       |
    | url              | text        | YES  |     | NULL              |       |
    | asr_status       | tinyint(2)  | YES  | MUL | 1                 |       |
    | create_time      | datetime    | YES  |     | CURRENT_TIMESTAMP |       |
    +------------------+-------------+------+-----+-------------------+-------+
    """

    msg_id = mongoengine.StringField(primary_key=True, verbose_name="消息ID")
    user_id = mongoengine.StringField(verbose_name="员工ID", max_length=64)
    external_user_id = mongoengine.StringField(verbose_name="客户ID", max_length=64)
    union_id = mongoengine.StringField(verbose_name="UNION_ID", max_length=64)
    talk_time = mongoengine.IntField(verbose_name="通话时间（秒）")
    call_type = mongoengine.IntField(verbose_name="1 主叫 2 被叫")
    start_time = mongoengine.DateTimeField(verbose_name="开始时间")
    end_time = mongoengine.DateTimeField(verbose_name="结束时间")
    url = mongoengine.StringField(verbose_name="链接地址")
    create_time = mongoengine.DateTimeField(verbose_name="结束时间")
    asr_status = mongoengine.IntField(
        verbose_name="语音转录状态", help_text="语音转录状态  1待转录 2转录中 3转录成功 4转录失败"
    )

    messages = mongoengine.EmbeddedDocumentListField(
        WecomMeetingVoiceMeta, verbose_name="所有对话记录"
    )

    meta = {
        "collection": "wecom_meeting_voice",
        "indexes": [
            "#msg_id",
            "#user_id",
            "#external_user_id",
            "#union_id",
            "call_type",
            "start_time",
        ],
        "abstract": True,
    }

    def __str__(self):
        return self.msg_id

import json
from typing import List

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class CallCenterVoiceMeta(mongoengine.DynamicEmbeddedDocument):
    start_time = mongoengine.IntField(verbose_name="开始时间")
    end_time = mongoengine.IntField(verbose_name="开始时间")
    text = mongoengine.StringField(verbose_name="对话内容")
    from_role = mongoengine.StringField(verbose_name="发送人角色")

    def __str__(self):
        return f"[{self.start_time}-{self.end_time}] {self.text}"

    @classmethod
    def get_meta_list_from_asr_result(
        cls, asr_result: str
    ) -> List["CallCenterVoiceMeta"]:
        try:
            data = json.loads(asr_result)
            result = []
            for i in data:
                result.append(
                    cls(
                        start_time=i["Begin"],
                        end_time=i["End"],
                        text=i["Words"],
                        from_role=i["Role"],
                    )
                )
                return result
        except json.JSONDecodeError:
            return []


class CallCenter(mongoengine.DynamicDocument, MultiDatabaseMixin):
    id = mongoengine.IntField(verbose_name="主键", primary_key=True)
    start_time = mongoengine.DateTimeField(verbose_name="通话开始时间", null=True)
    end_time = mongoengine.DateTimeField(verbose_name="通话结束时间", null=True)
    customer_id = mongoengine.StringField(
        verbose_name="指向bnail_sys_user id  客服id", null=True
    )
    customer_name = mongoengine.StringField(verbose_name="客服名字", null=True)
    talk_time = mongoengine.StringField(verbose_name="通话时间（分钟）", null=True)
    call_type = mongoengine.IntField(verbose_name="1 主叫 2 被叫", null=True)
    usr_user_id = mongoengine.StringField(verbose_name="用户id", null=True)
    mkt_user_id = mongoengine.StringField(verbose_name="", null=True)
    user_phone = mongoengine.StringField(verbose_name="用户手机号", null=True)
    record_url = mongoengine.StringField(verbose_name="通话录音文件地址（上传到七牛）", null=True)
    create_time = mongoengine.DateTimeField(null=True)
    update_time = mongoengine.DateTimeField(null=True)
    contact_id = mongoengine.StringField(verbose_name="录音id", null=True)
    talk_entrance = mongoengine.IntField(verbose_name="", null=True)
    qa_score = mongoengine.IntField(verbose_name="质检得分", null=True)
    connid = mongoengine.StringField(verbose_name="通话id", null=True)
    username = mongoengine.StringField(verbose_name="用户昵称", null=True)
    update_call_rec = mongoengine.IntField(verbose_name="1 已更新通话记录0 未更新", null=True)
    contact_disposition = mongoengine.IntField(
        verbose_name="电话结束原因",
        null=True,
        help_text="电话结束原因，参考枚举类型 ContactDisposition， "
        "Success(0) 正常,  NoAnswer(1) 无应答,  Rejected(2)拒绝, Busy(3)忙, AbandonedInContactFlow(4) IVR呼损, "
        "AbandonedInQueue(5)队列呼损, AbandonedRing(6) 久振不接,  QueueOverflow(7) 等待超时被挂断",
    )
    update_qauality_check_phrase = mongoengine.IntField(
        verbose_name="1 已更新通话文本信息,0 未更新", null=True
    )
    quality_check_phrase = mongoengine.EmbeddedDocumentListField(
        CallCenterVoiceMeta, verbose_name="通话文本信息", null=True
    )
    type = mongoengine.IntField(verbose_name="0.阿里云,1.udesk,2.腾讯云", null=True)
    remark = mongoengine.StringField(verbose_name="备注说明", null=True)
    as_case = mongoengine.IntField(verbose_name="是否加入案例库", null=True)
    operator = mongoengine.StringField(verbose_name="操作人", null=True)
    operator_id = mongoengine.IntField(verbose_name="操作人ID", null=True)
    processing_status = mongoengine.IntField(verbose_name="", null=True)
    last_handle_time = mongoengine.DateTimeField(verbose_name="最近处理时间", null=True)
    sync_time = mongoengine.DateTimeField(verbose_name="同步时间", null=True)
    main_key = mongoengine.StringField(verbose_name="lians主键", null=True)

    meta = {
        "collection": "call_center",
        "indexes": [
            "start_time",
            "end_time",
            "#customer_id",
            "#customer_name",
            "#usr_user_id",
            "#user_phone",
            "#username",
        ],
        "abstract": True,
    }

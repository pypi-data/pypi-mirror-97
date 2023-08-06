from itertools import chain

try:
    from wechatpy.work.client.api import WeChatDepartment
except ImportError:
    from wechatpy.enterprise.client.api import WeChatDepartment


class WeChatDepartmentChild(WeChatDepartment):
    def get_users_map_relation(self, id=None, key="name", status=0, fetch_child=0):
        """
        映射员工某详细字段到 ``user_id``

        获取员工user_id 和某些字段的映射字典

        id: 部门 id， 如果不填，默认获取有权限的所有部门
        key: 员工详细信息字段 key
        status: 0 获取全部员工，1 获取已关注成员列表，
                2 获取禁用成员列表，4 获取未关注成员列表。可叠加
        fetch_child: 1/0：是否递归获取子部门下面的成员
        dict - 部门成员user_id到指定字段 的 map  ``{ user_id：key }``
        """
        ids = [id] if id is not None else [item["id"] for item in self.get()]
        users_info = list(
            chain(
                *[
                    self.get_users(
                        department, status=status, fetch_child=fetch_child, simple=False
                    )
                    for department in ids
                ]
            )
        )
        users_zip = [(user["userid"], user[key]) for user in users_info]
        return dict(users_zip)

# -*- coding: utf-8 -*-
# @Time : 2024/8/20 17:40
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_info_base.py
# @Project : Viewer
from ..cgt_base import MyCGTeamWork


class CGTInfoBase(MyCGTeamWork):
    def __init__(self, project_db: str):
        """
            INFO 基类
        """
        super().__init__()
        self.project_db = project_db

# -*- coding: utf-8 -*-
# @Time : 2024/7/30 下午2:06
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : account_id_data.py
# @Project : create_shot_new
import dataclasses
from enum import Enum
from typing import List, Optional


class TDAccount(Enum):
    wangshuo = "3B6A9F22-35B0-E371-3300-393DF36B8600"
    zhuyihan = "45291132-7377-4A9E-7CAB-DD112A99ADFB"


@dataclasses.dataclass
class AccountData:
    id: str
    name: str
    cn_name: Optional[str]
    department: Optional[str]
    image: Optional[List[dict]]

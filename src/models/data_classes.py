# -*- coding: utf-8 -*-
# @Time : 2024/8/14 13:22
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : data_classes.py
# @Project : Viewer
from typing import *
from dataclasses import dataclass
from .custom_types import *
from enum import Enum


class UserAuthority(Enum):
    User = "user"
    Group = "group"
    Leader = "leader"
    Supervisor = "supervisor"


class UserType(Enum):
    Common = "common"
    CGTeamwork = "cgTeamwork"


@dataclass
class User:
    _id: Optional[UserID]
    name: str
    password: Optional[str]
    department: str
    authority: UserAuthority
    user_type: UserType

    def __iter__(self):
        return iter((self.name, self.password, self.department, self.authority, self.user_type))

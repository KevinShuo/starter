# -*- coding: utf-8 -*-
# @Time : 2024/8/21 10:42
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : dataclass.py
# @Project : Viewer
import dataclasses


@dataclasses.dataclass
class AssetInfo:
    asset_entity: str
    asset_type: str

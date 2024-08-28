# -*- coding: utf-8 -*-
# @Time : 2024/7/29 下午2:17
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : shot_data.py
# @Project : create_shot_new
import dataclasses


@dataclasses.dataclass
class ShotData:
    """
        创建镜头需要的数据类
    """
    episode: str
    shot_number: str
    frame: str
    source_name: str
    source_path: str
    view_path: str


@dataclasses.dataclass
class ShotDirPath:
    iplate: str
    retime: str
    aux: str

# -*- coding: utf-8 -*-
# @Time : 2024/8/20 16:57
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : project.py
# @Project : Viewer

from ..cgt_info_base import CGTInfoBase
from .dataclass import *


class CGTAssetProject(CGTInfoBase):
    def __init__(self, project_db: str):
        super().__init__(project_db)

    def get_all_assets(self):
        """
            获取这个项目内所有的资产信息

        Returns:

        """
        id_list = self.t_tw.info.get_id(db=self.project_db, module=self.module, filter_list=[])
        if not id_list:
            raise AttributeError('No assets found')
        task_data = self.t_tw.info.get(db=self.project_db, module=self.module, id_list=id_list,
                                       field_sign_list=["asset_type.entity", "asset.entity"])
        assets = tuple(
            sorted([AssetInfo(asset_type=i.get("asset_type.entity"), asset_entity=i.get("asset.entity")) for i in
                    task_data], key=lambda x: x.asset_entity))
        return assets

    @property
    def module(self) -> str:
        return "asset"

# -*- coding: utf-8 -*-
# @Time : 2024/8/5 上午10:54
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_asset_type.py
# @Project : asset_publish
from ..cgt_info_base import CGTInfoBase
from typing import NewType, Tuple

AssetType = NewType('AssetType', str)


class CGTAssetTypeInfo(CGTInfoBase):
    def __init__(self, project_db: str):
        super().__init__(project_db)

    def get_asset_type(self) -> Tuple[AssetType, ...]:
        """
            获取该项目的所有资产类型

        :return:
        """
        asset_type_id_list = self.t_tw.info.get_id(db=self.project_db, module=self.module, filter_list=[])
        asset_type_data = self.t_tw.info.get(db=self.project_db, module=self.module, id_list=asset_type_id_list,
                                             field_sign_list=["asset_type.entity"])

        return tuple(sorted([AssetType(i["asset_type.entity"]) for i in asset_type_data]))

    @property
    def module(self):
        return "asset_type"

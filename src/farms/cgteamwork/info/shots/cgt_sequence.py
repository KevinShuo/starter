# -*- coding: utf-8 -*-
# @Time : 2024/8/5 上午11:15
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_sequence.py
# @Project : asset_publish
from ..cgt_info_base import CGTInfoBase
from typing import NewType, Tuple

SequenceInfo = NewType('SequenceInfo', str)


class CGTSequenceInfo(CGTInfoBase):
    def __init__(self, project_db: str):
        super().__init__(project_db)

    def get_all_sequences(self) -> Tuple[SequenceInfo, ...]:
        """
            获取所有场次

        :return:
        """
        seq_id_list = self.t_tw.info.get_id(db=self.project_db, module=self.module, filter_list=[])
        seq_dict_list = self.t_tw.info.get(db=self.project_db, module=self.module, id_list=seq_id_list,
                                           field_sign_list=['seq.entity'])
        return tuple(sorted([SequenceInfo(i["seq.entity"]) for i in seq_dict_list]))

    @property
    def module(self):
        return "seq"

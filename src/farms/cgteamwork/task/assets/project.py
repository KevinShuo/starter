# -*- coding: utf-8 -*-
from ..cgt_task_base import *


class CGTTaskProject(CGTTaskBase):
    def __init__(self, project_db: str):
        super().__init__(project_db)
        self.cgt_account = CGTAccount()

    def get_assets_for_pipeline_and_asset_type(self, asset_type: str, pipeline: PipelineEnum, with_my_tasks: bool):
        """
            根据流程以及资产类型获取任务信息

        :param asset_type: 资产类型
        :param pipeline: 流程
        :param with_my_tasks: 是否获取我的任务
        :return:
        """
        fileds = self.t_tw.task.fields(self.project_db, self.module)
        if with_my_tasks:
            current_user_name = self.cgt_account.current_user
            id_list = self.t_tw.task.get_id(self.project_db, self.module,
                                            filter_list=[["asset_type.entity", "=", asset_type], "and",
                                                         ["task.account", "=", current_user_name], "and",
                                                         ["pipeline.entity", "=", pipeline.value]])
        else:
            id_list = self.t_tw.task.get_id(self.project_db, self.module,
                                            filter_list=[["asset_type.entity", "=", asset_type], "and",
                                                         ["pipeline.entity", "=", pipeline.value]])
        tasks = self.t_tw.task.get(self.project_db, self.module, id_list, field_sign_list=fileds)
        return tuple(sorted([AssetTaskData(task_name=i["task.entity"],
                                           asset_name=i["asset.entity"],
                                           pipeline=i["pipeline.entity"],
                                           task_account=i["task.account"],
                                           task_status=i["task.status"],
                                           task_cn_name=i["asset.cn_name"],
                                           asset_type=i["asset_type.entity"],
                                           task_id=i["id"],
                                           task_artist=i["task.artist"]) for i in tasks],
                            key=lambda x: x.task_name))

    def get_my_tasks(self):
        """
            获取所有我的资产
        Returns:

        """
        fileds = self.t_tw.task.fields(self.project_db, self.module)
        current_user_name = self.cgt_account.current_user
        id_list = self.t_tw.task.get_id(self.project_db, self.module,
                                        filter_list=[["task.account", "=", current_user_name], "and",
                                                     ["task.status", "!in", ["Internal Final", "omitted"]]])
        tasks = self.t_tw.task.get(self.project_db, self.module, id_list, field_sign_list=fileds)
        return tuple([AssetTaskData(task_name=i["task.entity"],
                                    asset_name=i["asset.entity"],
                                    pipeline=i["pipeline.entity"],
                                    task_account=i["task.account"],
                                    task_status=i["task.status"],
                                    task_cn_name=i["asset.cn_name"],
                                    asset_type=i["asset_type.entity"],
                                    task_id=i["id"],
                                    task_artist=i["task.artist"]) for i in tasks])

    @property
    def module(self):
        return "asset"

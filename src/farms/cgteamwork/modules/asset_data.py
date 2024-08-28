# -*- coding: utf-8 -*-
# @Time : 2024/8/5 下午12:00
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : asset_data.py
# @Project : asset_publish
import dataclasses
from enum import Enum


@dataclasses.dataclass
class AssetTaskData:
    """
    Data class representing the task information for an asset.

    Attributes:
        asset_name (str): The name of the asset.
        task_name (str): The name of the task.
        pipeline (str): The pipeline associated with the task.
        task_account (str): The account responsible for the task.
        task_status (str): The current status of the task.
        task_cn_name (str): The Chinese name of the task.
        asset_type (str): The type of the asset.
        task_id (str): The unique identifier for the task.
        task_artist (str): The artist assigned to the task.
    """
    asset_name: str
    task_name: str
    pipeline: str
    task_account: str
    task_status: str
    task_cn_name: str
    asset_type: str
    task_id: str
    task_artist: str

    def __str__(self):
        return (f"{'=' * 40}\n"
                f"Asset Name: {self.asset_name}\n"
                f"Task Name: {self.task_name}\n"
                f"Pipeline: {self.pipeline}\n"
                f"Task Account: {self.task_account}\n"
                f"Task Status: {self.task_status}\n"
                f"Task Chinese Name: {self.task_cn_name}\n"
                f"Asset Type: {self.asset_type}\n"
                f"Task ID: {self.task_id}\n"
                f"Task Artist: {self.task_artist}\n"
                f"{'=' * 40}")

    def __repr__(self):
        return (f"AssetTaskData(asset_name={self.asset_name!r}, task_name={self.task_name!r}, "
                f"pipeline={self.pipeline!r}, task_account={self.task_account!r}, "
                f"task_status={self.task_status!r}, task_cn_name={self.task_cn_name!r}, "
                f"asset_type={self.asset_type!r}, task_id={self.task_id!r}, "
                f"task_artist={self.task_artist!r})")

    def __eq__(self, other):
        if not isinstance(other, AssetTaskData):
            return NotImplemented
        return (self.asset_name == other.asset_name and
                self.task_name == other.task_name and
                self.pipeline == other.pipeline and
                self.task_account == other.task_account and
                self.task_status == other.task_status and
                self.task_cn_name == other.task_cn_name and
                self.asset_type == other.asset_type and
                self.task_id == other.task_id and
                self.task_artist == other.task_artist)

    def __hash__(self):
        return hash((self.asset_name, self.task_name, self.pipeline, self.task_account, self.task_status,
                     self.task_cn_name, self.asset_type, self.task_id, self.task_artist))


class PipelineEnum(Enum):
    Mod = "Mod"
    Shader = "Shader"
    Rig = "Rig"

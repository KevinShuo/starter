import typing
from typing import Tuple

from . import cgt_base
from .modules import project_data
from .modules.project_data import ProjectData


class CGTProjectsData(cgt_base.MyCGTeamWork):
    """
        CGT 操作全局类
    """

    def __init__(self):
        super().__init__()

    def get_all_active_projects(self) -> Tuple[ProjectData, ...]:
        """
            获取所有激活的项目
            
        :return 项目数据类 元组
        """
        all_fields = self.t_tw.info.fields(db="public", module="project")
        id_list = self.t_tw.info.get_id(db="public", module="project", filter_list=[["project.status", "=", "Active"]])
        datas = self.t_tw.info.get(db="public", module="project", id_list=id_list,
                                   field_sign_list=all_fields)

        return tuple(sorted([project_data.ProjectData(name=data["project.entity"],
                                                      full_name=data["project.full_name"],
                                                      status=data["project.status"],
                                                      database=data["project.database"],
                                                      image=data["project.image"],
                                                      frame_rate=data["project.frame_rate"],
                                                      resolution=data["project.resolution"]) for data in datas],
                            key=lambda x: x.name))

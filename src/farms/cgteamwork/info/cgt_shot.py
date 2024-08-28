# -*- coding: utf-8 -*-
# @Time : 2024/7/29 下午2:04
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_shot.py
# @Project : create_shot_new
import typing

from ..cgt_base import MyCGTeamWork
from ..modules.shot_data import ShotData, ShotDirPath
from ..errors import cgteamwork_error

shot_id = typing.NewType("shot_id", str)


class CGTShotInfo(MyCGTeamWork):
    def __init__(self, project_database: str, module: str):
        super().__init__()
        self.project_database = project_database
        self._module = module
        self._shot_id = None

    def create_shot(self, shot_data: ShotData) -> typing.Optional[shot_id]:
        """
            创建镜头

        :param shot_data: 要创建镜头的数据
        :return: 成功放回True 失败返回False
        """
        if (not shot_data.shot_number or not shot_data.frame or not shot_data.episode or not shot_data.source_name
                or not shot_data.source_path or not shot_data.view_path):
            raise cgteamwork_error.CreateShotAttributeIncomplete
        if not self.check_shot_exists(shot_data):
            raise cgteamwork_error.ShotNumberIsExists
        info_task_id = self.t_tw.info.create(db=self.project_database, module=self.module,
                                             sign_data_dict={f"{self.module}.entity": shot_data.shot_number,
                                                             "eps.entity": shot_data.episode,
                                                             f"{self.module}.frame": str(shot_data.frame),
                                                             f"{self.module}.source_name": shot_data.source_name,
                                                             f"{self.module}.source": shot_data.source_path},
                                             is_return_id=True)
        rt = self.t_tw.info.set_image(db=self.project_database, module=self.module, id_list=[info_task_id],
                                      field_sign=f"{self.module}.image", img_path=shot_data.view_path, compress="720")
        if not rt:
            return

        return shot_id(info_task_id)

    def check_shot_exists(self, shot_data: ShotData) -> bool:
        """
            检查镜头是否存在
        :param shot_data: 要创建镜头的数据
        :return: 如果镜头存在返回false,如果不存在返回true
        """
        shot_id = self.get_shot_id(shot_data)
        if shot_id:
            return False
        return True

    def get_shot_id(self, shot_data: ShotData) -> typing.Union[str, bool]:
        """
            获取镜头ID
        """
        shot_id = self.t_tw.info.get_id(db=self.project_database, module=self.module,
                                        filter_list=[[f"{self.module}.entity", "=", shot_data.shot_number], "and",
                                                     ["eps.entity", "=", shot_data.episode]])
        if shot_id:
            return shot_id[0]
        return False

    def get_shot_path(self) -> ShotDirPath:
        """
            获取镜头路径
        """
        iplate_path = typing.NewType("iplate_path", str)
        retime_path = typing.NewType("retime_path", str)
        aux_path = typing.NewType("aux_path", str)

        def _get_iplate() -> iplate_path:
            """
                获取底图
            """
            iplate_path = self.t_tw.info.get_sign_filebox(self.project_database, self.module, self.shot_id,
                                                          filebox_sign=f"{self.module}_iplate")["Path"]
            return iplate_path

        def _get_retime() -> retime_path:
            """
                获取变速
            """
            retime_path = self.t_tw.info.get_sign_filebox(self.project_database, self.module, self.shot_id,
                                                          filebox_sign=f"{self.module}_retime")["Path"]
            return retime_path

        def _get_aux() -> aux_path:
            """
                获取辅助素材

            """
            aux_path = self.t_tw.info.get_sign_filebox(self.project_database, self.module, self.shot_id,
                                                       filebox_sign=f"{self.module}_aux_elements")["Path"]
            return aux_path

        iplate = _get_iplate()
        retime = _get_retime()
        aux = _get_aux()
        return ShotDirPath(iplate, retime, aux)

    def send_message(self, account_id: list, content: str) -> bool:
        """
            发生信息到指定账号上

        :param account_id: 接受消息的账号ID列表
        :param content: 信息内容
        :return: 成功 True 失败 False
        """
        return self.t_tw.info.send_msg(self.project_database, self.module, self.shot_id, account_id, content)

    def get_fps(self) -> int:
        id_list = self.t_tw.info.get_id(db="public", module="project",
                                        filter_list=[["project.status", "=", "Active"], "and",
                                                     ["project.database", "=", self.project_database]])
        pd = self.t_tw.info.get(db="public", module="project", id_list=id_list,
                                field_sign_list=["project.frame_rate"])
        if not pd:
            raise cgteamwork_error.ProjectHasNotFrameRate
        try:
            fps = int(pd[0]["project.frame_rate"])
            return fps
        except Exception:
            raise Exception("invalid frame rate")

    @property
    def module(self):
        return self._module

    @property
    def shot_id(self) -> shot_id:
        if not self._shot_id:
            raise AttributeError("Shot ID is not set")
        return shot_id(self._shot_id)

    @shot_id.setter
    def shot_id(self, shot_ida: str):
        self._shot_id = shot_id(shot_ida)

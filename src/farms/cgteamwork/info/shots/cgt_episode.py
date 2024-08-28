import typing

from ..cgt_info_base import CGTInfoBase


class CGTEpisodeInfo(CGTInfoBase):
    """
        CGT 操作集数类
    """

    def __init__(self, project_database: str):
        super().__init__(project_database)

    def add_episode(self, episode: str) -> typing.Union[str, bool]:
        """
            添加一个集数
            
        :param episode: 集数名称
        """
        eps_id = self.t_tw.info.create(self.project_db, self.module, sign_data_dict={"eps.entity": episode},
                                       is_return_id=True)
        if not episode:
            return False
        return eps_id

    def delete_episode(self, eps: str) -> bool:
        """
            删除集数
            
        :param eps: 集数名称
        """
        r = self.check_eps_exists(eps)
        if r:
            b = self.t_tw.info.delete(self.project_db, self.module, id_list=[r])
            return b
        return False

    def check_eps_exists(self, eps: str) -> typing.Union[str, bool]:
        """
            检查集数是否存在
            
        :param eps: 集数名称
        :return: 如果集数存在返回ID，不存在返回False
        """
        id_list = self.t_tw.info.get_id(db=self.project_db, module=self.module,
                                        filter_list=[["eps.entity", "=", eps]])
        if not id_list:
            return False
        return id_list[0]

    @property
    def module(self):
        return "eps"

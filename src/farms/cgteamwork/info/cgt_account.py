# -*- coding: utf-8 -*-
# @Time : 2024/8/5 上午11:48
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_account.py
# @Project : asset_publish
import json
from typing import Tuple

from ..cgt_base import MyCGTeamWork
from ..errors import cgteamwork_error
from ..modules.account_id_data import AccountData


class CGTAccount(MyCGTeamWork):
    def __init__(self):
        super().__init__()

    def get_current_user(self) -> AccountData:
        """
            获取当前用户

        :return:
        """
        login = self.t_tw.login()
        data = self.get_one_account(login.account())
        return data

    def get_one_account(self, account: str) -> AccountData:
        """
        根据账户名称获取一个账户的数据。

        :param account: CGT账户
        :return: 返回一个 AccountData 实例，其中包含账户的详细信息
        :raises cgteamwork_error.HasNotThisAccount: 如果没有找到匹配的账户，则抛出该异常
        """
        fields = self.t_tw.info.fields(self.project_database, self.module)
        id_list = self.t_tw.info.get_id(self.project_database, self.module,
                                        filter_list=[["account.status", "=", "Y"], "and",
                                                     ["account.entity", "=", account]])
        if not id_list:
            raise cgteamwork_error.HasNotThisAccount
        data = self.t_tw.info.get(self.project_database, self.module, id_list=id_list,
                                  field_sign_list=fields)[0]
        return AccountData(id=data['account.id'],
                           name=data['account.entity'],
                           cn_name=data["account.name"],
                           department=data['account.department'],
                           image=json.loads(data["account.image"] if data["account.image"] else None))

    def get_all_accounts(self) -> Tuple[AccountData, ...]:
        """
            获取所有激活账号信息
        :return:
        """
        fields = self.t_tw.info.fields(self.project_database, self.module)
        id_list = self.t_tw.info.get_id(self.project_database, self.module, filter_list=[["account.status", "=", "Y"]])
        data_list = self.t_tw.info.get(self.project_database, self.module, id_list=id_list,
                                       field_sign_list=fields)
        return tuple(sorted([AccountData(id=data["account.id"],
                                         name=data["account.entity"],
                                         cn_name=data["account.name"],
                                         department=data["account.department"],
                                         image=json.loads(data["account.image"])
                                         if data["account.image"] else "") for data in data_list],
                            key=lambda x: x.name))

    @property
    def current_user(self) -> str:
        a = self.get_current_user()
        return a.name

    @property
    def project_database(self) -> str:
        return "public"

    @property
    def module(self) -> str:
        return "account"

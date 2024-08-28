# -*- coding: utf-8 -*-
# @Time : 2024/7/29 下午2:05
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : cgt_base.py
# @Project : create_shot_new
import sys
from typing import Optional

cgt_version = 6
try:
    sys.path.append(f"C:/CgTeamWork_v{cgt_version}/bin/base")
    import cgtw2

    try:
        import py39lib.ctlib as ctlib
    except:
        import py3lib.ctlib as ctlib
except ImportError:
    raise ImportError('Please install cgtw2 package')
from .errors import cgteamwork_error


class MyCGTeamWork:
    def __init__(self):
        try:
            self.t_tw = cgtw2.tw()
        except:
            raise cgteamwork_error.HasNotLoginCGTeamwork

    def download_image(self, server_path: str, local_path: str) -> Optional[str]:
        """
        从服务器下载图片
        :param server_path:服务器路径
        :param local_path:本地报错路径
        :return:
        """
        t_http_ip = self.t_tw.login.http_server_ip()
        t_token = self.t_tw.login.token()
        t_http = ctlib.http(t_http_ip, t_token)
        t_result = t_http.download(server_path, local_path)
        if not t_result:
            return
        return local_path

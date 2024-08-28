# -*- coding: utf-8 -*-
# @Time : 2024/8/14 9:43
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : logging_config.py
# @Project : Viewer
import os
import logging
from datetime import datetime


def setup_logging(log_file_path='logs/app.log'):
    # 获取当前日期并格式化为文件名的一部分
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file_path_with_date = f'logs/app_{date_str}.log'

    # 确保日志目录存在
    if not os.path.exists(os.path.dirname(log_file_path_with_date)):
        os.makedirs(os.path.dirname(log_file_path_with_date), exist_ok=True)

    # 配置日志
    logging.basicConfig(
        filename=log_file_path_with_date,
        filemode='a',  # 'w' 表示每次启动程序时清空日志文件，'a' 表示追加日志
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

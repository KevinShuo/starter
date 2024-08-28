# -*- coding: utf-8 -*-
# @Time : 2024/8/13 15:12
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : util.py
# @Project : Viewer
import inspect
import os
from functools import wraps

# from models.custom_types import Path
from src.config import g_plugin_name
from src.models.custom_types import Path


def get_app_plugin_path(plugin_name: str) -> Path:
    app_data = os.getenv('APPDATA')
    plugin_base_path = os.path.join(app_data, plugin_name)
    if not os.path.exists(plugin_base_path):
        os.makedirs(plugin_base_path)
    return Path(plugin_base_path)


def get_user_path() -> Path:
    app_path = get_app_plugin_path(g_plugin_name)
    user_path = os.path.join(app_path, 'Users').replace('\\', '/')
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return Path(user_path)


def get_startup_path() -> Path:
    app_path = get_app_plugin_path(g_plugin_name)
    user_path = os.path.join(app_path, 'Startup').replace('\\', '/')
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return Path(user_path)


def get_config_path() -> Path:
    return Path(os.path.join(os.path.dirname(__file__), 'config').replace('\\', '/'))


def log_caller(func):
    @wraps(func)  # 保留原始函数的元数据
    def wrapper(*args, **kwargs):
        # 获取调用此函数的函数名
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            caller_name = caller_frame.f_code.co_name
            print(f"{func.__name__} was called by {caller_name}")
        finally:
            del frame  # 明确删除引用，以防止循环引用

        # 调用原始函数并返回其结果
        return func(*args, **kwargs)

    return wrapper

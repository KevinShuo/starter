# -*- coding: utf-8 -*-
import dataclasses
import os
import re
from typing import Optional


@dataclasses.dataclass
class MaxVersion:
    version: str
    path: str


def check_version(target_path: str, version: str) -> Optional[MaxVersion]:
    if not os.path.exists(target_path) or not os.path.isdir(target_path):
        raise FileNotFoundError
    file_list = os.listdir(target_path)
    if not file_list:
        raise FileNotFoundError
    sort_version = sorted(file_list, key=lambda x: re.search(r"v(\d+)", x).group(1), reverse=True)
    max_version = re.search(r"v(\d+)", sort_version[0]).group(1)
    if compare_versions(version, max_version) == -1:
        return MaxVersion(max_version, os.path.join(target_path, sort_version[0]).replace("\\", "/"))


def compare_versions(local_version: str, server_version: str) -> int:
    local_parts = list(map(int, local_version.split(".")))
    server_parts = list(map(int, server_version.split(".")))

    while len(local_parts) < len(server_parts):
        local_parts.append(0)
    while len(server_parts) < len(local_parts):
        server_parts.append(0)

    # 逐部分比较
    for local, server in zip(local_parts, server_parts):
        if local < server:
            return -1  # 本地版本较旧
        elif local > server:
            return 1  # 本地版本较新

    return 0  # 版本相同

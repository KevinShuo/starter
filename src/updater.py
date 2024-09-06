# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import sys
import time


class Updater:
    def __init__(self):
        self.exe_path = sys.executable
        self.src_path = None
        self.dst_path = None

    def run(self):
        if self.src_path is None or self.dst_path is None:
            raise AttributeError('src_path and dst_path must be set')
        self.close_program(self.exe_path)
        self.replace_directory(self.src_path, self.dst_path)
        self.restart_program(self.exe_path)

    def set_src_path(self, src_path: str):
        self.src_path = src_path

    def set_dst_path(self, dst_path: str):
        self.dst_path = dst_path

    def close_program(self, exe_name):
        os.system(f'taskkill /f /im {exe_name}')

    def replace_directory(self, src, dst):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)

    def restart_program(self, exe_path):
        subprocess.Popen([exe_path])



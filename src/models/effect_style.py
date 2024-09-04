# -*- coding: utf-8 -*-
import ctypes
from ctypes import windll, byref
from ctypes.wintypes import DWORD, BOOL

# 定义 Windows API 函数和常量
DWM_BB_ENABLE = 0x1
DWM_BB_BLURREGION = 0x2
DWM_BB_TRANSITIONONMAXIMIZED = 0x4


class DWM_BLURBEHIND(ctypes.Structure):
    _fields_ = [('dwFlags', DWORD),
                ('fEnable', BOOL),
                ('hRgnBlur', ctypes.c_void_p),
                ('fTransitionOnMaximized', BOOL)]


dwmapi = windll.dwmapi
user32 = windll.user32


def apply_blur_effect(hwnd):
    bb = DWM_BLURBEHIND()
    bb.dwFlags = DWM_BB_ENABLE | DWM_BB_BLURREGION | DWM_BB_TRANSITIONONMAXIMIZED
    bb.fEnable = True
    bb.hRgnBlur = None  # 使整个窗口都具有模糊效果
    bb.fTransitionOnMaximized = True
    dwmapi.DwmEnableBlurBehindWindow(hwnd, byref(bb))

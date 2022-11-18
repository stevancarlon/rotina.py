import sys
from cx_Freeze import setup, Executable

# from PyQt5 import uic, QtGui, QtCore
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from plyer import notification
# from PIL import Image
# import sys, time, pyttsx3, ast, re, pystray
# import ctypes
# import win32gui, win32con
# from pynput.keyboard import Key, Controller


build_exe_options = {"packages":["PyQt5", "plyer", "PIL", "sys", "time", "pyttsx3", "ast", "re", "pystray", "ctypes", "win32gui", "win32con", "pynput"], "excludes":[]}


# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="rotina",
    version="0.1",
    description="Schedule your routine.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="icon.ico")],
)

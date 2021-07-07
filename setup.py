#!/usr/bin/env python
# coding: utf-8


from cx_Freeze import setup, Executable
import sys,os

build_exe_options = {"packages": ["os"], "includes":["tkinter", "tkinter.ttk"]}
base=None

if sys.platform == "win32":
	base = "Win32GUI"


setup(name="Timer",
      version="1.0",
      description="Countdown timer",
	  options = {"build_exe": build_exe_options},
      executables=[Executable("Timer.py", base=base, icon = "chronometer.ico")]
      )

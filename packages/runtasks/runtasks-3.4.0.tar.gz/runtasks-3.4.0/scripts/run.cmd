@echo off
rem = """-*-Python-*- script
python -x "%~f0" %*
exit /b %errorlevel%
"""
from runtasks.cmdline import run
run()

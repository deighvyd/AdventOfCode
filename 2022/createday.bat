@echo off
setlocal enabledelayedexpansion

copy day.py.template day%1.py
echo. > day%1.input
echo. > day%1.input.test
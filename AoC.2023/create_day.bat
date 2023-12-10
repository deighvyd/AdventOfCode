@echo off
setlocal enabledelayedexpansion

set /p "DayNum=Enter Day Number: "
set DayCSFile=Day%DayNum%.cs
if exist %DayCSFile% (
	echo %DayCSFile% alredy exists!
	goto eof
)

copy Day.cs.template %DayCSFile%

pushd data
echo. > day%DayNum%.1.test
echo. > day%DayNum%.1.input
echo. > day%DayNum%.2.test
echo. > day%DayNum%.2.input
popd

:eof
echo %CMDCMDLINE% | findstr /C:"/c">nul && pause
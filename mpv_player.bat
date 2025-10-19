@echo off
:loop
set /p video_url=Enter video URL (Exit = 0):
if %video_url%==0 (
    exit
)
mpvnet "%video_url%"
goto loop
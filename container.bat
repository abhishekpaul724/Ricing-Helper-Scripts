@echo off
set CONTAINER=container-name

REM Check container state
for /f "tokens=*" %%i in ('podman inspect -f "{{.State.Running}}" %CONTAINER% 2^>nul') do set STATE=%%i

if "%STATE%"=="true" (
    echo Container is running. Stopping...
    podman stop %CONTAINER%
    echo Stopped.
) else (
    echo Container is stopped. Starting...
    podman start %CONTAINER%
    echo Started.
)
pause
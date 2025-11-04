@echo off
set PODNAME=pod-name

for /f "tokens=*" %%i in ('podman pod inspect -f "{{.State}}" %PODNAME% 2^>nul') do set STATE=%%i

if "%STATE%"=="Running" (
    echo Pod is running. Stopping...
    podman pod stop %PODNAME%
    echo Stopped.
) else (
    echo  Pod is stopped. Starting...
    podman pod start %PODNAME%
    podman start miniflux-db
    podman start miniflux
    echo Started.
)
pause
@echo off
chcp 1251 >nul
color 9
echo ������������� ������ ���� Monifactory

setlocal
set normalCfgPath=%~dp0config-overrides\normal
set hardCfgPath=%~dp0config-overrides\hardmode
set harderCfgPath=%~dp0config-overrides\harder
set targetPath=%~dp0config

echo �������� ����� ����:
echo �: �������
echo �: �������
echo �: ����� �������
choice /c ��� /m "��� �� ��������:"

if "%errorlevel%" == "1" goto copyNormal
if "%errorlevel%" == "2" goto copyHard
if "%errorlevel%" == "3" goto copyHarder

:copyNormal
robocopy "%normalCfgPath%" "%targetPath%" *.* /e /nfl /ndl

rem If server.properties exists, update server config
IF EXIST server.properties (move "%targetPath%\server.properties" .\)
echo normal > .mode
goto end

:copyHard
robocopy "%hardCfgPath%" "%targetPath%" *.* /e /nfl /ndl

rem If server.properties exists, update server config
IF EXIST server.properties (move "%targetPath%\server.properties" .\)
echo hard > .mode
goto end

:copyHarder
robocopy "%hardCfgPath%" "%targetPath%" *.* /e /nfl /ndl
robocopy "%harderCfgPath%" "%targetPath%" *.* /e /nfl /ndl

rem If server.properties exists, update server config
IF EXIST server.properties (move "%targetPath%\server.properties" .\)
echo harder > .mode
goto end

:end
rem if server.properties is left over in the config path, remove it
IF EXIST "%targetPath%/server.properties" DEL "%targetPath%\server.properties"
echo ����� ���������
pause
exit

@echo off
chcp 65001 > nul
REM 双击启动入口：调用同目录的 PowerShell 脚本
PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
echo.
echo 脚本执行完毕。后端/前端已在新窗口运行。
pause

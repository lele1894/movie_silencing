@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 视频音频提取与空白视频生成工具

echo.
echo ========================================
echo   视频音频提取与空白视频生成工具
echo ========================================
echo.

REM 检查是否提供了输入文件参数
if "%~1"=="" (
    echo 使用方法:
    echo   双击运行此脚本，然后按提示输入文件路径
    echo   或者直接拖拽视频文件到此脚本上
    set /p input_video="请输入视频文件路径: "
) else (
    set "input_video=%~1"
)

REM 检查输入文件是否存在
if not exist "!input_video!" (
    echo 错误: 找不到输入文件 "!input_video!"
    echo.
    pause
    exit /b 1
)

REM 获取文件信息
for %%F in ("!input_video!") do (
    set "file_dir=%%~dpF"
    set "file_name=%%~nF"
    set "file_ext=%%~xF"
)

REM 设置输出文件路径
set "output_video=!file_dir!!file_name!_blank!file_ext!"

echo.
echo 输入文件: !input_video!
echo 输出文件: !output_video!
echo.

REM 运行Python脚本
python "%~dp0提取音频并创建一个空白视频.py" "!input_video!" "!output_video!"

REM 检查Python脚本执行结果
if !errorlevel! neq 0 (
    echo.
    echo 错误: Python脚本执行失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 处理完成!
echo ========================================
echo.

pause
@echo off
chcp 65001
cls
echo ========================================
echo  GitHub上传助手 - Intel AI PC比赛作品
echo ========================================
echo.

REM 设置项目路径
set PROJECT_PATH=e:\interest\contest\modelscope\Intel AI PC-openclaw
cd /d "%PROJECT_PATH%"

echo 当前路径: %CD%
echo.

REM 检查Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到Git，请先安装Git
    pause
    exit /b 1
)

echo [1/5] Git检查通过
echo.

REM 获取GitHub用户名
echo ========================================
echo 请输入您的GitHub用户名:
echo ========================================
set /p GITHUB_USER="用户名: "

if "%GITHUB_USER%"=="" (
    echo [错误] 用户名不能为空
    pause
    exit /b 1
)

echo.
echo [2/5] 配置远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/ai-pc-private-art-assistant.git

echo [3/5] 检查远程仓库...
git remote -v

echo.
echo [4/5] 准备推送代码...
git branch -M main

echo.
echo ========================================
echo 即将推送代码到GitHub
echo 仓库地址: https://github.com/%GITHUB_USER%/ai-pc-private-art-assistant
echo ========================================
echo.
echo 按任意键开始推送...
pause >nul

echo.
echo [5/5] 推送代码到GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  上传成功！
    echo ========================================
    echo.
    echo 您的GitHub仓库地址:
    echo https://github.com/%GITHUB_USER%/ai-pc-private-art-assistant
    echo.
    echo 请复制此链接用于比赛提交
    echo.
) else (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. GitHub仓库不存在 - 请先创建仓库
    echo 2. 网络连接问题
    echo 3. 认证问题 - 需要登录GitHub
    echo.
    echo 请检查后重试
)

echo.
pause

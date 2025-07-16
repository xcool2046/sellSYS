@echo off
echo 正在启动销售管理系统客户端...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查虚拟环境是否存在
if not exist "client_venv" (
    echo 创建虚拟环境...
    python -m venv client_venv
)

REM 激活虚拟环境
call client_venv\Scripts\activate.bat

REM 安装依赖
echo 检查并安装依赖...
pip install -r client/requirements.txt

REM 启动客户端
echo.
echo 启动客户端应用...
python run_client.py

REM 如果客户端退出，保持窗口打开
echo.
echo 客户端已关闭
pause
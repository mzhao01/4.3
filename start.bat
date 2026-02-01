@echo off

REM 安装依赖
pip install -r requirements.txt

REM 启动服务
uvicorn api.main:app --host 0.0.0.0 --port 8000
#!/bin/bash
echo "=================================="
echo "     启动 MCP Servers"
echo "=================================="

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "错误: 虚拟环境不存在"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 加载环境变量
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 获取端口配置，使用默认值
FILE_ANALYZER_PORT=${MCP_FILE_ANALYZER_PORT:-8001}
SQLITE_PORT=${MCP_SQLITE_PORT:-8002}

echo "启动 File Analyzer Server (端口: $FILE_ANALYZER_PORT)..."
python servers/file_analyzer/server.py &
PID_FILE=$!

echo "启动 SQLite Agent Server (端口: $SQLITE_PORT)..."
python servers/sqlite_agent/sqlite_server.py &
PID_SQLITE=$!

# 等待进程
wait $PID_FILE $PID_SQLITE
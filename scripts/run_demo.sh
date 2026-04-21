#!/bin/bash
set -e
echo "=================================="
echo "       启动 MCP Demo"
echo "=================================="

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "错误: 虚拟环境不存在，请先运行 ./scripts/setup.sh"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "错误: .env 文件不存在，请先运行 ./scripts/setup.sh"
    exit 1
fi

# 启动 MCP Servers
echo "启动 MCP Servers..."
./scripts/run_all_servers.sh &
SERVER_PID=$!

# 等待服务启动
echo "等待服务启动..."
sleep 3

# 启动 Streamlit
echo "启动 Streamlit Web UI..."
streamlit run app/main.py --server.port 8501

# 清理
trap "kill $SERVER_PID 2>/dev/null" EXIT
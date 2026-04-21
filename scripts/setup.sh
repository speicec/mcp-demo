#!/bin/bash
set -e
echo "初始化 MCP Demo 环境..."

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ "$PYTHON_VERSION" < "3.10" ]]; then
    echo "错误: 需要 Python 3.10+"
    exit 1
fi
echo "Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -e ".[dev]"

# 创建数据目录
mkdir -p demo_data

# 初始化数据库
if [ -f "demo_data/init_schema.sql" ]; then
    echo "初始化数据库..."
    sqlite3 demo_data/demo.db < demo_data/init_schema.sql
fi

# 复制环境变量模板
if [ ! -f ".env" ]; then
    echo "复制 .env.example 到 .env..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的 ANTHROPIC_API_KEY"
fi

echo ""
echo "环境初始化完成！"
echo "下一步："
echo "  1. 编辑 .env 文件，设置 ANTHROPIC_API_KEY"
echo "  2. 运行 ./scripts/run_demo.sh 启动演示"
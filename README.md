# MCP Demo

> 展示 Agent 从"问答"到"执行"的跨越 —— MCP 生态演示项目

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-org/mcp-demo.git
cd mcp-demo
```

### 2. 配置环境

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 3. 设置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 ANTHROPIC_API_KEY
```

### 4. 启动演示

```bash
./scripts/run_demo.sh
```

## 项目结构

- `servers/` - MCP Server 实现
- `app/` - Streamlit Web UI
- `demo_data/` - 演示数据

## 演示场景

1. **数据分析**：Agent 分析 CSV 文件，生成报告并存入数据库
2. **日志诊断**：Agent 解析日志文件，识别异常并生成诊断报告

## 许可证

MIT
# MCP Demo

> 展示 Agent 从"问答"到"执行"的跨越 -- MCP 生态演示项目

本项目演示了如何使用 Model Context Protocol (MCP) 让 AI Agent 具备真正的执行能力：自主读取文件、分析数据、存储结果。

## 项目目标

通过 MCP 工具链，Agent 可以：

- **自主读取文件** -- 无需人工复制粘贴，直接访问本地文件系统
- **自主分析数据** -- 解析 CSV/JSON 等格式，执行统计分析
- **自主存储结果** -- 将分析结果持久化到 SQLite 数据库
- **生成结构化报告** -- 输出格式化的分析报告

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
# 启动所有 MCP Server
./scripts/run_all_servers.sh

# 或单独运行演示
./scripts/run_demo.sh
```

## 项目结构

```
mcp-demo/
├── servers/                 # MCP Server 实现
│   ├── file_analyzer/       # 文件分析服务
│   │   ├── server.py        # MCP Server 入口
│   │   └── tools.py        # 工具函数实现
│   └── sqlite_agent/        # SQLite 数据库服务
│       ├── sqlite_server.py # MCP Server 入口
│       └── tools.py         # 工具函数实现
├── app/                     # Streamlit Web UI
│   ├── main.py              # 应用主入口
│   ├── components/          # UI 组件
│   │   ├── sidebar.py       # 侧边栏配置
│   │   ├── task_panel.py    # 任务面板
│   │   └── result_display.py# 结果展示
│   └── utils/               # 工具函数
│       └── demo_scenarios.py# 演示场景定义
├── demo_data/               # 演示数据
│   ├── sample_sales.csv     # 销售数据样例
│   ├── sample_logs.json     # 日志数据样例
│   ├── init_schema.sql      # 数据库初始化脚本
│   └── demo.db              # SQLite 数据库
├── docs/                    # 文档
│   ├── ARCHITECTURE.md      # 架构说明
│   └── DEMO_GUIDE.md        # 演示指南
└── scripts/                 # 运行脚本
    ├── setup.sh             # 环境设置
    ├── run_demo.sh           # 运行演示
    └── run_all_servers.sh    # 启动所有服务
```

## MCP Server 功能表

### file-analyzer

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `read_file` | 读取文件内容，支持 CSV/JSON/文本格式 | `filepath`: 文件路径 |
| `analyze_csv` | 分析 CSV 文件，生成统计信息 | `filepath`: 文件路径, `columns`: 可选列名列表 |
| `get_file_stats` | 获取文件基本信息（大小、类型、行数） | `filepath`: 文件路径 |

### sqlite-agent

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `execute_query` | 执行 SQL 查询，返回 JSON 格式结果 | `query`: SQL 语句 |
| `create_table` | 创建数据表 | `table_name`: 表名, `columns`: 列定义 |
| `insert_data` | 插入数据记录 | `table_name`: 表名, `data`: 键值对数据 |
| `get_table_schema` | 获取表结构信息 | `table_name`: 表名 |
| `list_tables` | 列出数据库中所有表 | 无 |

## 演示场景

### 1. 数据分析场景

Agent 自主完成以下流程：

1. 使用 `read_file` 读取 `demo_data/sample_sales.csv`
2. 使用 `analyze_csv` 分析销售数据统计
3. 使用 `create_table` 创建结果存储表
4. 使用 `insert_data` 保存分析结果

### 2. 日志诊断场景

Agent 自主完成以下流程：

1. 使用 `read_file` 读取 `demo_data/sample_logs.json`
2. 解析日志内容，识别异常条目
3. 生成诊断报告并存储

### 3. 自定义任务

通过 Streamlit Web UI 或 Claude Code 下达自定义任务，Agent 将根据需求调用相应的 MCP 工具完成。

## 相关资源

- [MCP Protocol 文档](https://modelcontextprotocol.io/) -- Model Context Protocol 官方规范
- [Claude Code](https://claude.ai/code) -- Anthropic 官方 AI 编程助手
- [架构说明](./docs/ARCHITECTURE.md) -- 项目架构设计详解
- [演示指南](./docs/DEMO_GUIDE.md) -- 详细演示操作指南

## 许可证

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
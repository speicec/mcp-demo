# MCP Demo 系统架构

本文档描述 MCP Demo 项目的系统架构设计。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户界面层                               │
│                     Streamlit Web UI                            │
│                    (app/main.py)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Agent 层                                  │
│                   Claude Agent                                  │
│           (anthropic SDK, tool calling)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Protocol 层                             │
│                  Model Context Protocol                         │
│              (工具发现、调用、结果返回)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  File Analyzer   │ │   SQLite Agent   │ │  Demo Dashboard  │
│    Server        │ │     Server       │ │     Server       │
│  (Port 8001)     │ │   (Port 8002)    │ │   (Port 8003)    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         数据层                                   │
│            SQLite Database / 文件系统                            │
│                  (demo_data/)                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 各层详解

### 1. 用户界面层 (Streamlit Web UI)

**职责**: 提供交互式 Web 界面，展示 Agent 执行过程

**组件**:
- `app/main.py` - 主应用入口
- `app/components/sidebar.py` - 侧边栏配置
- `app/components/task_panel.py` - 任务面板
- `app/components/result_display.py` - 结果展示
- `app/utils/demo_scenarios.py` - 演示场景定义

**功能**:
- 展示可用演示场景
- 实时显示 Agent 执行过程
- 展示工具调用链和结果
- 支持用户自定义任务输入

### 2. Agent 层 (Claude Agent)

**职责**: 核心智能决策层，理解用户意图并协调工具执行

**技术栈**:
- Anthropic Claude API
- Tool Calling 机制
- 流式响应处理

**工作流程**:
1. 接收用户任务
2. 分析任务，选择合适的工具
3. 通过 MCP 协议调用工具
4. 处理工具返回结果
5. 迭代执行直到任务完成
6. 生成最终回复

### 3. MCP Protocol 层

**职责**: 标准化工具接口，实现服务发现和调用

**核心概念**:
- **Server**: 提供一组相关工具的服务
- **Tool**: 单个可执行功能单元
- **Resource**: 可访问的数据资源

**协议流程**:
```
Client                        Server
  │                              │
  │─── initialize ──────────────>│
  │<── server info ─────────────│
  │                              │
  │─── list_tools ──────────────>│
  │<── tools list ──────────────│
  │                              │
  │─── call_tool ───────────────>│
  │<── tool result ──────────────│
```

### 4. MCP Server 层

#### 4.1 File Analyzer Server

**功能**: 文件分析和处理

**工具**:
- `analyze_csv` - CSV 文件分析
- `analyze_json` - JSON 文件分析
- `analyze_log` - 日志文件分析
- `get_file_info` - 获取文件元信息

**端口**: 8001

#### 4.2 SQLite Agent Server

**功能**: SQLite 数据库操作

**工具**:
- `execute_query` - 执行 SQL 查询
- `list_tables` - 列出数据库表
- `describe_table` - 描述表结构
- `insert_data` - 插入数据

**端口**: 8002

### 5. 数据层

**存储**:
- `demo_data/demo.db` - SQLite 数据库
- `demo_data/sample_sales.csv` - 销售数据样例
- `demo_data/sample_logs.json` - 日志数据样例

## 数据流

### 场景1: 数据分析流程

```
用户输入 "分析销售数据"
    │
    ▼
Streamlit UI 接收任务
    │
    ▼
Agent 解析意图
    │
    ├──> 调用 file_analyzer/get_file_info
    │         │
    │         ▼
    │    获取 sample_sales.csv 信息
    │
    ├──> 调用 file_analyzer/analyze_csv
    │         │
    │         ▼
    │    分析数据，生成统计
    │
    ├──> 调用 sqlite_agent/insert_data
    │         │
    │         ▼
    │    将结果存入数据库
    │
    ▼
Agent 生成分析报告
    │
    ▼
Streamlit UI 展示结果
```

### 场景2: 日志诊断流程

```
用户输入 "诊断日志异常"
    │
    ▼
Agent 调用 file_analyzer/analyze_log
    │
    ▼
识别 ERROR、WARNING 级别日志
    │
    ▼
Agent 生成诊断建议
    │
    ▼
结果展示
```

## 设计原则

1. **模块化**: 每个 MCP Server 独立部署，职责单一
2. **可扩展**: 新增 Server 无需修改现有代码
3. **标准化**: 遵循 MCP 协议规范
4. **可观测**: 完整的执行日志和追踪

## 部署架构

### 开发环境

```bash
# 终端1: File Analyzer Server
python servers/file_analyzer/server.py

# 终端2: SQLite Agent Server
python servers/sqlite_agent/sqlite_server.py

# 终端3: Streamlit UI
streamlit run app/main.py
```

### 生产环境建议

- 使用 Docker 容器化各服务
- 使用 Nginx 反向代理
- 添加认证和授权层
- 配置日志聚合和监控
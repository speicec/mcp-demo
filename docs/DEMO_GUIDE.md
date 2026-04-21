# MCP Demo 演示指南

本指南帮助您快速体验 MCP Demo 的核心功能。

## 环境准备

### 系统要求

- Python 3.10+
- SQLite 3
- 网络访问（用于 Claude API）

### 快速安装

```bash
# 1. 克隆项目
git clone https://github.com/your-org/mcp-demo.git
cd mcp-demo

# 2. 运行安装脚本
./scripts/setup.sh

# 3. 配置 API Key
# 编辑 .env 文件，设置 ANTHROPIC_API_KEY
```

### 手动安装

如果自动脚本无法运行，可手动执行：

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e ".[dev]"

# 初始化数据库
sqlite3 demo_data/demo.db < demo_data/init_schema.sql

# 复制环境变量模板
cp .env.example .env
# 编辑 .env 设置 ANTHROPIC_API_KEY
```

## 启动演示

### 方式一：一键启动（推荐）

```bash
./scripts/run_demo.sh
```

此脚本会自动：
1. 启动所有 MCP Server
2. 启动 Streamlit Web UI
3. 打开浏览器访问 http://localhost:8501

### 方式二：分别启动

```bash
# 终端1: 启动 MCP Servers
./scripts/run_all_servers.sh

# 终端2: 启动 Streamlit
source .venv/bin/activate
streamlit run app/main.py
```

## 演示场景

### 场景1: 销售数据分析

**目标**: 展示 Agent 如何分析 CSV 数据并存入数据库

**步骤**:
1. 在 Web UI 侧边栏选择 "销售数据分析"
2. 点击 "执行任务"
3. 观察 Agent 执行过程：
   - 读取 `sample_sales.csv`
   - 分析销售趋势和统计信息
   - 将结果存入 SQLite 数据库
4. 查看最终分析报告

**预期输出**:
```
📊 销售数据分析报告

数据概览:
- 总记录数: 50
- 时间范围: 2024-01 至 2024-03
- 产品类别: 5 类

销售统计:
- 总销售额: ¥1,234,567
- 平均订单: ¥24,691
- 最高单品: 产品A ¥89,000

趋势分析:
- 1月: 增长 15%
- 2月: 增长 8%
- 3月: 下降 3%
```

### 场景2: 日志异常诊断

**目标**: 展示 Agent 如何解析日志并识别问题

**步骤**:
1. 选择 "日志异常诊断" 场景
2. 执行任务
3. Agent 会：
   - 读取 `sample_logs.json`
   - 识别 ERROR 和 WARNING 级别日志
   - 分析异常模式
   - 生成诊断建议

**预期输出**:
```
🔍 日志诊断报告

异常统计:
- ERROR: 3 条
- WARNING: 5 条
- INFO: 42 条

关键问题:
1. [ERROR] 数据库连接超时 (出现 2 次)
   建议: 检查数据库连接池配置

2. [ERROR] 内存使用超过 90%
   建议: 优化缓存策略，考虑增加内存

3. [WARNING] API 响应时间 > 3s
   建议: 启用响应缓存
```

### 场景3: 自定义任务

**目标**: 展示 Agent 的灵活任务处理能力

**示例任务**:
- "查询数据库中所有表的结构"
- "统计销售数据中的产品分布"
- "找出日志中所有 ERROR 信息"

**步骤**:
1. 在任务输入框输入自定义任务
2. 点击执行
3. 查看 Agent 执行过程和结果

## 演示亮点

### 1. 实时执行可视化

Web UI 实时展示：
- Agent 思考过程
- 工具调用链
- 每步执行结果
- 最终答案生成

### 2. 工具调用透明

每个工具调用都显示：
- 工具名称
- 输入参数
- 执行时间
- 返回结果

### 3. 多工具协作

演示 Agent 如何：
- 自主选择合适的工具
- 组合多个工具完成复杂任务
- 处理工具调用失败情况

### 4. 错误处理

展示 Agent 如何：
- 处理无效输入
- 重试失败操作
- 提供有用的错误信息

## 常见问题

### Q: API Key 配置错误

确保 `.env` 文件中 `ANTHROPIC_API_KEY` 已正确设置：

```bash
cat .env | grep ANTHROPIC_API_KEY
```

### Q: 端口被占用

检查并修改 `.env` 中的端口配置：

```bash
MCP_FILE_ANALYZER_PORT=8001
MCP_SQLITE_PORT=8002
STREAMLIT_PORT=8501
```

### Q: 数据库初始化失败

手动初始化：

```bash
sqlite3 demo_data/demo.db < demo_data/init_schema.sql
```

### Q: 依赖安装失败

尝试使用国内镜像：

```bash
pip install -e ".[dev]" -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 停止演示

按 `Ctrl+C` 停止运行中的服务。

## 下一步

- 查看源代码了解实现细节
- 阅读 `docs/ARCHITECTURE.md` 了解系统设计
- 尝试添加新的 MCP Server
- 扩展演示场景
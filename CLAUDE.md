# CLAUDE.md

本项目是一个 MCP 生态演示项目，展示 Agent 如何通过 MCP 工具链执行任务。

## 开发指南

### MCP Server 开发规范

每个 MCP Server 位于 `servers/<name>/` 目录，包含：
- `server.py`: MCP Server 主入口，定义 server 实例
- `tools.py`: 工具定义，每个工具是一个独立函数

### 工具定义示例

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="analyze_file",
            description="分析文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                },
                "required": ["filepath"],
            },
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_file":
        result = await analyze_file(arguments["filepath"])
        return [TextContent(type="text", text=result)]
```

### 测试规范

- 每个 Server 必须有对应的测试文件
- 使用 pytest-asyncio 测试异步代码
- 测试覆盖率要求 >= 80%

### Commit 规范

使用约定式提交：
- `feat: 添加新功能`
- `fix: 修复 bug`
- `docs: 文档更新`
- `test: 测试相关`
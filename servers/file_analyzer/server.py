# servers/file_analyzer/server.py
"""文件分析 MCP Server - 提供文件读取和分析工具"""
from mcp.server import Server
from mcp.types import Tool, TextContent

from servers.file_analyzer.tools import (
    read_file,
    analyze_csv,
    get_file_stats,
)

server = Server("file-analyzer")


@server.list_tools()
async def list_tools():
    """列出所有可用工具"""
    return [
        Tool(
            name="read_file",
            description="读取文件内容，支持文本、CSV、JSON 格式",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "文件路径"},
                },
                "required": ["filepath"],
            },
        ),
        Tool(
            name="analyze_csv",
            description="分析 CSV 文件，返回统计摘要",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "CSV 文件路径"},
                    "columns": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["filepath"],
            },
        ),
        Tool(
            name="get_file_stats",
            description="获取文件基本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "文件路径"},
                },
                "required": ["filepath"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具调用"""
    try:
        if name == "read_file":
            result = await read_file(arguments["filepath"])
        elif name == "analyze_csv":
            result = await analyze_csv(
                arguments["filepath"], arguments.get("columns")
            )
        elif name == "get_file_stats":
            result = await get_file_stats(arguments["filepath"])
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"执行错误: {str(e)}")]
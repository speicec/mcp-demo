# servers/sqlite_agent/sqlite_server.py
"""SQLite MCP Server - 提供数据库操作工具"""
import sqlite3
from pathlib import Path

from mcp.server import Server
from mcp.types import TextContent, Tool

from servers.sqlite_agent.tools import (
    create_table,
    execute_query,
    get_table_schema,
    insert_data,
    list_tables,
)

DATABASE_PATH = Path(__file__).parent.parent.parent.parent / "demo_data" / "demo.db"

server = Server("sqlite-agent")


@server.list_tools()
async def list_tools():
    """列出所有可用工具"""
    return [
        Tool(
            name="execute_query",
            description="执行 SQL 查询",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL 查询语句"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="create_table",
            description="创建数据表",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名"},
                    "columns": {"type": "string", "description": "列定义，如 'id INTEGER PRIMARY KEY, name TEXT'"},
                },
                "required": ["table_name", "columns"],
            },
        ),
        Tool(
            name="insert_data",
            description="插入数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名"},
                    "data": {"type": "object", "description": "要插入的数据，键为列名，值为数据"},
                },
                "required": ["table_name", "data"],
            },
        ),
        Tool(
            name="get_table_schema",
            description="获取表结构",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名"},
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="list_tables",
            description="列出数据库中所有表",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具调用"""
    # 先检查工具名称，避免不必要地连接数据库
    if name not in ("execute_query", "create_table", "insert_data", "get_table_schema", "list_tables"):
        return [TextContent(type="text", text=f"未知工具: {name}")]

    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        if name == "execute_query":
            result = execute_query(conn, arguments["query"])
        elif name == "create_table":
            result = create_table(conn, arguments["table_name"], arguments["columns"])
        elif name == "insert_data":
            result = insert_data(conn, arguments["table_name"], arguments["data"])
        elif name == "get_table_schema":
            result = get_table_schema(conn, arguments["table_name"])
        elif name == "list_tables":
            result = list_tables(conn)
        conn.close()
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"执行错误: {str(e)}")]
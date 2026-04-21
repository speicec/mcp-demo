# servers/sqlite_agent/tests/test_server.py
"""SQLite MCP Server 测试"""
import json
import os
import sqlite3
import tempfile

import pytest


@pytest.mark.asyncio
async def test_list_tools():
    """测试工具列表包含预期工具"""
    from servers.sqlite_agent.sqlite_server import list_tools

    tools = await list_tools()
    assert len(tools) >= 3
    tool_names = [t.name for t in tools]
    assert "execute_query" in tool_names
    assert "create_table" in tool_names
    assert "insert_data" in tool_names
    assert "get_table_schema" in tool_names
    assert "list_tables" in tool_names


@pytest.fixture
def temp_db():
    """创建临时数据库，测试后自动清理"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        filepath = f.name
    conn = sqlite3.connect(filepath)
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES ('Alice')")
    conn.commit()
    conn.close()
    yield filepath
    # 清理临时文件
    try:
        os.unlink(filepath)
    except Exception:
        pass


@pytest.mark.asyncio
async def test_execute_query_select(temp_db):
    """测试 SELECT 查询"""
    from servers.sqlite_agent.tools import execute_query

    conn = sqlite3.connect(temp_db)
    result = execute_query(conn, "SELECT * FROM test")
    conn.close()
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["name"] == "Alice"


@pytest.mark.asyncio
async def test_execute_query_insert(temp_db):
    """测试 INSERT 查询"""
    from servers.sqlite_agent.tools import execute_query

    conn = sqlite3.connect(temp_db)
    result = execute_query(conn, "INSERT INTO test (name) VALUES ('Bob')")
    conn.close()
    assert "成功" in result


@pytest.mark.asyncio
async def test_create_table(temp_db):
    """测试创建表"""
    from servers.sqlite_agent.tools import create_table

    conn = sqlite3.connect(temp_db)
    result = create_table(conn, "new_table", "id INTEGER PRIMARY KEY, value TEXT")
    conn.close()
    assert "成功" in result or "创建成功" in result


@pytest.mark.asyncio
async def test_insert_data(temp_db):
    """测试插入数据"""
    from servers.sqlite_agent.tools import insert_data

    conn = sqlite3.connect(temp_db)
    result = insert_data(conn, "test", {"name": "Charlie"})
    conn.close()
    assert "成功" in result


@pytest.mark.asyncio
async def test_get_table_schema(temp_db):
    """测试获取表结构"""
    from servers.sqlite_agent.tools import get_table_schema

    conn = sqlite3.connect(temp_db)
    result = get_table_schema(conn, "test")
    conn.close()
    data = json.loads(result)
    assert len(data) == 2  # id and name columns
    column_names = [col["列名"] for col in data]
    assert "id" in column_names
    assert "name" in column_names


@pytest.mark.asyncio
async def test_list_tables(temp_db):
    """测试列出所有表"""
    from servers.sqlite_agent.tools import list_tables

    conn = sqlite3.connect(temp_db)
    result = list_tables(conn)
    conn.close()
    data = json.loads(result)
    assert "test" in data


@pytest.mark.asyncio
async def test_call_tool_execute_query(temp_db):
    """测试通过 call_tool 调用 execute_query"""
    import servers.sqlite_agent.sqlite_server as server_module

    # 保存原始 DATABASE_PATH 并替换
    old_path = server_module.DATABASE_PATH
    server_module.DATABASE_PATH = temp_db

    try:
        # 使用模块中的 call_tool 函数，它会使用修改后的 DATABASE_PATH
        result = await server_module.call_tool("execute_query", {"query": "SELECT * FROM test"})
        assert len(result) == 1
        data = json.loads(result[0].text)
        assert len(data) == 1
    finally:
        server_module.DATABASE_PATH = old_path


@pytest.mark.asyncio
async def test_call_tool_list_tables(temp_db):
    """测试通过 call_tool 调用 list_tables"""
    import servers.sqlite_agent.sqlite_server as server_module

    old_path = server_module.DATABASE_PATH
    server_module.DATABASE_PATH = temp_db

    try:
        result = await server_module.call_tool("list_tables", {})
        assert len(result) == 1
        data = json.loads(result[0].text)
        assert "test" in data
    finally:
        server_module.DATABASE_PATH = old_path


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """测试调用未知工具"""
    from servers.sqlite_agent.sqlite_server import call_tool

    result = await call_tool("unknown_tool", {})
    assert "未知工具" in result[0].text
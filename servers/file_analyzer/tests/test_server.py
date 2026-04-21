# servers/file_analyzer/tests/test_server.py
"""文件分析 MCP Server 测试"""
import json
import os
import tempfile

import pytest


@pytest.mark.asyncio
async def test_list_tools():
    """测试工具列表包含预期工具"""
    from servers.file_analyzer.server import list_tools

    tools = await list_tools()
    assert len(tools) >= 2
    tool_names = [t.name for t in tools]
    assert "read_file" in tool_names
    assert "analyze_csv" in tool_names


@pytest.fixture
def sample_csv():
    """创建示例 CSV 文件"""
    content = "name,age,salary\nAlice,30,50000\nBob,25,45000\nCarol,35,60000"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        return f.name


@pytest.fixture
def sample_json():
    """创建示例 JSON 文件"""
    content = '{"name": "test", "value": 42}'
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(content)
        return f.name


@pytest.mark.asyncio
async def test_analyze_csv(sample_csv):
    """测试 CSV 分析功能"""
    from servers.file_analyzer.tools import analyze_csv

    result = await analyze_csv(sample_csv)
    data = json.loads(result)
    assert data["行数"] == 3
    assert "列信息" in data
    assert "name" in data["列信息"]


@pytest.mark.asyncio
async def test_get_file_stats(sample_csv):
    """测试文件统计功能"""
    from servers.file_analyzer.tools import get_file_stats

    result = await get_file_stats(sample_csv)
    data = json.loads(result)
    assert data["类型"] == "CSV"


@pytest.mark.asyncio
async def test_read_file_csv(sample_csv):
    """测试 CSV 文件读取"""
    from servers.file_analyzer.tools import read_file

    result = await read_file(sample_csv)
    assert "CSV 文件" in result
    assert "3 行" in result


@pytest.mark.asyncio
async def test_read_file_json(sample_json):
    """测试 JSON 文件读取"""
    from servers.file_analyzer.tools import read_file

    result = await read_file(sample_json)
    parsed = json.loads(result)
    assert parsed["name"] == "test"


@pytest.mark.asyncio
async def test_read_file_not_found():
    """测试文件不存在的情况"""
    from servers.file_analyzer.tools import read_file

    result = await read_file("/nonexistent/path/file.txt")
    assert "文件不存在" in result


@pytest.mark.asyncio
async def test_call_tool_read_file(sample_csv):
    """测试通过 call_tool 调用 read_file"""
    from servers.file_analyzer.server import call_tool

    result = await call_tool("read_file", {"filepath": sample_csv})
    assert len(result) == 1
    assert "CSV 文件" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """测试调用未知工具"""
    from servers.file_analyzer.server import call_tool

    result = await call_tool("unknown_tool", {})
    assert "未知工具" in result[0].text


# 清理临时文件
@pytest.fixture(autouse=True)
def cleanup(sample_csv, sample_json):
    """测试完成后清理临时文件"""
    yield
    try:
        os.unlink(sample_csv)
    except Exception:
        pass
    try:
        os.unlink(sample_json)
    except Exception:
        pass
# servers/sqlite_agent/tools.py
"""SQLite 工具实现"""
import json
import re
import sqlite3


def validate_identifier(name: str) -> str:
    """验证 SQL 标识符（表名/列名），防止 SQL 注入"""
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        raise ValueError(f"非法标识符: {name}")
    return name


def execute_query(conn: sqlite3.Connection, query: str) -> str:
    """执行 SQL 查询"""
    cursor = conn.execute(query)
    if query.strip().upper().startswith("SELECT"):
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return json.dumps(result, indent=2, ensure_ascii=False)
    else:
        conn.commit()
        return f"执行成功，影响 {cursor.rowcount} 行"


def create_table(conn: sqlite3.Connection, table_name: str, columns: str) -> str:
    """创建表"""
    validate_identifier(table_name)
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    conn.execute(sql)
    conn.commit()
    return f"表 {table_name} 创建成功"


def insert_data(conn: sqlite3.Connection, table_name: str, data: dict) -> str:
    """插入数据"""
    validate_identifier(table_name)
    for col in data.keys():
        validate_identifier(col)
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    values = list(data.values())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    conn.execute(sql, values)
    conn.commit()
    last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return f"数据插入成功，ID: {last_id}"


def get_table_schema(conn: sqlite3.Connection, table_name: str) -> str:
    """获取表结构"""
    validate_identifier(table_name)
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    schema = [
        {
            "列名": row[1],
            "类型": row[2],
            "非空": row[3] == 1,
            "默认值": row[4],
            "主键": row[5] == 1,
        }
        for row in rows
    ]
    return json.dumps(schema, indent=2, ensure_ascii=False)


def list_tables(conn: sqlite3.Connection) -> str:
    """列出所有表"""
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    return json.dumps(tables, indent=2, ensure_ascii=False)
# servers/file_analyzer/tools.py
"""文件分析工具实现"""
import json
from pathlib import Path
from typing import Optional

import pandas as pd


async def read_file(filepath: str) -> str:
    """读取文件内容"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    suffix = full_path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(full_path)
        return f"CSV 文件，{len(df)} 行，{len(df.columns)} 列\n列名: {list(df.columns)}"
    elif suffix == ".json":
        data = json.loads(full_path.read_text(encoding="utf-8"))
        return json.dumps(data, indent=2, ensure_ascii=False)
    else:
        content = full_path.read_text(encoding="utf-8")
        return content


async def analyze_csv(filepath: str, columns: Optional[list] = None) -> str:
    """分析 CSV 文件"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    df = pd.read_csv(full_path)
    if columns:
        df = df[columns]

    stats = {
        "文件": filepath,
        "行数": len(df),
        "列数": len(df.columns),
        "列信息": {}
    }

    for col in df.columns:
        col_data = df[col]
        col_stats = {
            "类型": str(col_data.dtype),
            "非空数": int(col_data.count())
        }
        if col_data.dtype in ["int64", "float64"]:
            col_stats["最小值"] = float(col_data.min())
            col_stats["最大值"] = float(col_data.max())
        stats["列信息"][col] = col_stats

    return json.dumps(stats, indent=2, ensure_ascii=False)


async def get_file_stats(filepath: str) -> str:
    """获取文件统计信息"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    size_kb = round(full_path.stat().st_size / 1024, 2)
    suffix = full_path.suffix.lower()

    file_type_map = {
        ".csv": "CSV",
        ".json": "JSON",
        ".txt": "文本",
        ".py": "Python",
        ".md": "Markdown"
    }
    file_type = file_type_map.get(suffix, "未知")

    content = full_path.read_text(encoding="utf-8")
    lines = len(content.split("\n"))

    return json.dumps(
        {
            "路径": filepath,
            "类型": file_type,
            "大小": f"{size_kb} KB",
            "行数": lines
        },
        indent=2,
        ensure_ascii=False
    )
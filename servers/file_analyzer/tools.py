# servers/file_analyzer/tools.py
"""文件分析工具实现"""
import json
from pathlib import Path
from typing import Optional

import pandas as pd

# 模块级常量
KB_FACTOR = 1024
NUMERIC_TYPES = ("int64", "float64")
FILE_TYPE_MAP = {
    ".csv": "CSV",
    ".json": "JSON",
    ".txt": "文本",
    ".py": "Python",
    ".md": "Markdown"
}


async def read_file(filepath: str) -> str:
    """读取文件内容"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    suffix = full_path.suffix.lower()
    if suffix == ".csv":
        try:
            df = pd.read_csv(full_path)
            return f"CSV 文件，{len(df)} 行，{len(df.columns)} 列\n列名: {list(df.columns)}"
        except pd.errors.EmptyDataError:
            return f"CSV 文件为空: {filepath}"
        except pd.errors.ParserError as e:
            return f"CSV 解析错误: {str(e)}"
        except Exception as e:
            return f"读取 CSV 文件失败: {str(e)}"
    elif suffix == ".json":
        try:
            data = json.loads(full_path.read_text(encoding="utf-8"))
            return json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return f"JSON 解析错误: {str(e)}"
        except UnicodeDecodeError:
            return f"文件编码错误，请确保文件使用 UTF-8 编码: {filepath}"
        except PermissionError:
            return f"无权限读取文件: {filepath}"
        except Exception as e:
            return f"读取 JSON 文件失败: {str(e)}"
    else:
        try:
            content = full_path.read_text(encoding="utf-8")
            return content
        except UnicodeDecodeError:
            return f"文件编码错误，请确保文件使用 UTF-8 编码: {filepath}"
        except PermissionError:
            return f"无权限读取文件: {filepath}"
        except Exception as e:
            return f"读取文件失败: {str(e)}"


async def analyze_csv(filepath: str, columns: Optional[list] = None) -> str:
    """分析 CSV 文件"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    try:
        df = pd.read_csv(full_path)
    except pd.errors.EmptyDataError:
        return f"CSV 文件为空: {filepath}"
    except pd.errors.ParserError as e:
        return f"CSV 解析错误: {str(e)}"
    except Exception as e:
        return f"读取 CSV 文件失败: {str(e)}"

    if columns:
        # 检查请求的列是否存在
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"请求的列不存在: {missing_cols}，可用列: {list(df.columns)}"
        try:
            df = df[columns]
        except Exception as e:
            return f"筛选列失败: {str(e)}"

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
        if col_data.dtype in NUMERIC_TYPES:
            col_stats["最小值"] = float(col_data.min())
            col_stats["最大值"] = float(col_data.max())
        stats["列信息"][col] = col_stats

    return json.dumps(stats, indent=2, ensure_ascii=False)


async def get_file_stats(filepath: str) -> str:
    """获取文件统计信息"""
    full_path = Path(filepath)
    if not full_path.exists():
        return f"文件不存在: {filepath}"

    try:
        size_kb = round(full_path.stat().st_size / KB_FACTOR, 2)
    except OSError as e:
        return f"获取文件大小失败: {str(e)}"

    suffix = full_path.suffix.lower()
    file_type = FILE_TYPE_MAP.get(suffix, "未知")

    try:
        content = full_path.read_text(encoding="utf-8")
        lines = len(content.split("\n"))
    except UnicodeDecodeError:
        return f"文件编码错误，请确保文件使用 UTF-8 编码: {filepath}"
    except PermissionError:
        return f"无权限读取文件: {filepath}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"

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
# app/main.py
"""MCP Demo Streamlit 主入口"""
from datetime import datetime
from typing import Dict, List, Tuple

import streamlit as st

from app.components.result_display import render_result_display
from app.components.sidebar import render_sidebar
from app.components.task_panel import render_task_panel

st.set_page_config(
    page_title="MCP Demo",
    page_icon="robot",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "execution_log" not in st.session_state:
    st.session_state.execution_log = []
if "final_result" not in st.session_state:
    st.session_state.final_result = ""


def simulate_execution(task_prompt: str) -> Tuple[List[Dict], str]:
    """模拟执行（用于演示）"""
    log = []
    log.append(
        {
            "timestamp": datetime.now().isoformat(),
            "tool": "read_file",
            "arguments": {"filepath": "demo_data/sample_sales.csv"},
            "output": "CSV 文件，10 行，5 列\n列名: ['date', 'product', 'region', 'quantity', 'revenue']",
        }
    )
    log.append(
        {
            "timestamp": datetime.now().isoformat(),
            "tool": "analyze_csv",
            "arguments": {"filepath": "demo_data/sample_sales.csv"},
            "output": '{"文件": "demo_data/sample_sales.csv", "行数": 10, "列数": 5}',
        }
    )
    log.append(
        {
            "timestamp": datetime.now().isoformat(),
            "tool": "insert_data",
            "arguments": {"table_name": "analysis_results", "data": {"analysis_type": "sales"}},
            "output": "数据插入成功，ID: 1",
        }
    )

    final_result = "销售数据分析完成！总销售额: $62,500，数据已存入数据库。"
    return log, final_result


def main():
    sidebar_config = render_sidebar()
    col_main, col_right = st.columns([3, 1])

    with col_main:
        task_config = render_task_panel(
            sidebar_config["scenario_name"], sidebar_config["scenario"]
        )

        if task_config["run_button"]:
            st.session_state.execution_log = []
            st.session_state.final_result = ""
            with st.spinner("Agent 正在执行任务..."):
                log, result = simulate_execution(task_config["task_prompt"])
                st.session_state.execution_log = log
                st.session_state.final_result = result
            st.rerun()

        if task_config["clear_button"]:
            st.session_state.execution_log = []
            st.session_state.final_result = ""
            st.rerun()

        render_result_display(
            st.session_state.execution_log, st.session_state.final_result
        )

    with col_right:
        st.subheader("MCP Server 状态")
        for s in [
            {"name": "file-analyzer", "status": "运行中", "port": 8001},
            {"name": "sqlite-agent", "status": "运行中", "port": 8002},
        ]:
            st.markdown(f"**{s['name']}** - {s['status']} (端口: {s['port']})")

        st.markdown("---")
        st.subheader("项目信息")
        st.markdown("- [架构文档](docs/ARCHITECTURE.md)\n- [演示指南](docs/DEMO_GUIDE.md)")


if __name__ == "__main__":
    main()
# app/components/result_display.py
"""结果展示组件"""
import json

import streamlit as st

from datetime import datetime


def render_result_display(execution_log: list, final_result: str):
    if not execution_log and not final_result:
        st.info("选择场景并点击「执行任务」开始演示")
        return

    if execution_log:
        st.subheader("执行过程")
        with st.expander("查看详细日志", expanded=True):
            for i, log in enumerate(execution_log, 1):
                timestamp = log.get("timestamp", datetime.now().isoformat())
                st.markdown(f"**步骤 {i}** - `{timestamp}`")
                if "tool" in log:
                    st.markdown(f"调用工具: `{log['tool']}`")
                    st.code(json.dumps(log.get("arguments", {}), indent=2, ensure_ascii=False), language="json")
                if "output" in log:
                    output = log["output"]
                    if len(output) > 500:
                        with st.expander("查看完整输出"):
                            st.code(output)
                    else:
                        st.code(output)
                st.markdown("---")

    if final_result:
        st.subheader("最终结果")
        st.success(final_result)
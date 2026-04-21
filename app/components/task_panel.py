# app/components/task_panel.py
"""任务面板组件"""
import streamlit as st


def render_task_panel(scenario_name: str, scenario: dict):
    st.header(f"{scenario_name}")

    if scenario_name == "自定义任务":
        task_prompt = st.text_area(
            "输入任务", height=200, placeholder="描述你想让 Agent 完成的任务..."
        )
    else:
        task_prompt = st.text_area("任务内容", value=scenario["prompt"], height=200, disabled=True)

    if scenario["expected_tools"]:
        st.markdown(
            "**预期使用的工具**: " + " ".join([f"`{t}`" for t in scenario["expected_tools"]])
        )

    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("执行任务", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("清除结果", use_container_width=True)

    return {"task_prompt": task_prompt, "run_button": run_button, "clear_button": clear_button}
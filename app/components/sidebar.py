# app/components/sidebar.py
"""侧边栏组件"""
import streamlit as st

from app.utils.demo_scenarios import get_scenario_list, get_scenario


def render_sidebar():
    with st.sidebar:
        st.title("MCP Demo")
        st.markdown("---")
        st.subheader("演示场景")
        scenario_name = st.selectbox("选择场景", get_scenario_list(), index=0)
        scenario = get_scenario(scenario_name)
        st.markdown(f"**描述**: {scenario['description']}")

        st.markdown("---")
        st.subheader("配置")
        api_key = st.text_input("Claude API Key", type="password")
        model = st.selectbox(
            "模型", ["claude-sonnet-4-6", "claude-opus-4-7", "claude-haiku-4-5"], index=0
        )

        st.markdown("---")
        st.subheader("执行控制")
        step_by_step = st.checkbox("逐步展示", value=True)

        return {
            "scenario_name": scenario_name,
            "scenario": scenario,
            "api_key": api_key,
            "model": model,
            "step_by_step": step_by_step,
        }
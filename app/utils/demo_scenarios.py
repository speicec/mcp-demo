# app/utils/demo_scenarios.py
"""演示场景定义"""
from typing import Dict, List

DEMO_SCENARIOS: Dict[str, Dict] = {
    "数据分析": {
        "description": "分析 CSV 销售数据，生成报告并存入数据库",
        "prompt": """请完成以下数据分析任务：

1. 读取 demo_data/sample_sales.csv 文件
2. 分析数据的统计特征（总销售额、各地区分布、产品销量排名）
3. 将分析结果存入数据库的 analysis_results 表
4. 生成一份简洁的分析报告""",
        "expected_tools": ["read_file", "analyze_csv", "execute_query", "insert_data"],
    },
    "日志诊断": {
        "description": "解析日志文件，识别异常并生成诊断报告",
        "prompt": """请完成以下日志诊断任务：

1. 读取 demo_data/sample_logs.json 文件
2. 筛选出 ERROR 和 WARN 级别的日志
3. 分析异常模式（哪些服务出错最多、错误类型分布）
4. 将异常记录存入 log_anomalies 表
5. 生成诊断报告""",
        "expected_tools": ["read_file", "execute_query", "insert_data"],
    },
    "自定义任务": {
        "description": "输入自定义任务，让 Agent 自主执行",
        "prompt": "",
        "expected_tools": [],
    },
}


def get_scenario_list() -> List[str]:
    return list(DEMO_SCENARIOS.keys())


def get_scenario(name: str) -> Dict:
    return DEMO_SCENARIOS.get(name, DEMO_SCENARIOS["自定义任务"])
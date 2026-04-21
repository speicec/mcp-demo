-- 创建分析结果表
CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    analysis_type TEXT NOT NULL,
    source_file TEXT,
    summary TEXT,
    metrics TEXT
);

-- 创建日志异常表
CREATE TABLE IF NOT EXISTS log_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
    log_timestamp TEXT,
    level TEXT,
    message TEXT,
    service TEXT,
    severity TEXT DEFAULT 'medium'
);

-- 创建指标统计表
CREATE TABLE IF NOT EXISTS daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE,
    total_revenue REAL,
    total_quantity INTEGER,
    top_product TEXT,
    top_region TEXT
);
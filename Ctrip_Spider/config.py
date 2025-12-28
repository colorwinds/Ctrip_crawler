"""
爬虫配置文件
用于统一管理反爬虫策略参数
"""
from typing import List, Tuple

# ==================== 延迟配置 ====================
# 请求延迟范围（秒）
DELAY_RANGE: Tuple[float, float] = (1, 3)

# 页面间额外延迟（秒）
PAGE_DELAY: float = 1.0

# ==================== User-Agent配置 ====================
# 是否启用User-Agent轮换
USE_USER_AGENT_ROTATION: bool = True

# User-Agent轮换模式: 'random' 或 'round_robin'
USER_AGENT_ROTATION_MODE: str = 'random'

# 自定义User-Agent列表（可选，如果为None则使用默认列表）
CUSTOM_USER_AGENTS: List[str] = None

# ==================== 代理配置 ====================
# 是否启用代理
USE_PROXY: bool = False

# 代理列表（格式: ['http://user:pass@host:port', ...]）
# 示例:
# PROXIES = [
#     'http://proxy1.example.com:8080',
#     'http://user:pass@proxy2.example.com:8080',
#     'socks5://proxy3.example.com:1080',
# ]
PROXIES: List[str] = []

# 代理检查超时时间（秒）
PROXY_CHECK_TIMEOUT: int = 5

# 代理失败阈值（超过此次数后标记为不活跃）
PROXY_MAX_FAILS: int = 3

# 代理测试URL
PROXY_TEST_URL: str = "https://www.baidu.com"

# ==================== 请求配置 ====================
# 请求超时时间（秒）
REQUEST_TIMEOUT: int = 10

# 最大重试次数
MAX_RETRIES: int = 3

# ==================== 日志配置 ====================
# 日志目录
LOG_DIR: str = "logs"

# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL: str = "INFO"

# ==================== 输出配置 ====================
# 数据输出目录
OUTPUT_DIR: str = "./Datasets"

# CSV文件编码
CSV_ENCODING: str = "utf-8-sig"

# JSON文件缩进
JSON_INDENT: int = 2


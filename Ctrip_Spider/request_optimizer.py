"""
请求优化器模块（兼容旧版本，推荐使用anti_spider.EnhancedRequestOptimizer）
"""
import random
import time
from typing import List, Tuple, Optional, Dict

# 处理相对导入和绝对导入
try:
    from .log import CtripSpiderLogger
except ImportError:
    # 直接运行时使用绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Ctrip_Spider.log import CtripSpiderLogger

# 导入新的增强版优化器
try:
    from .anti_spider import EnhancedRequestOptimizer, UserAgentPool, ProxyPool
except ImportError:
    try:
        from Ctrip_Spider.anti_spider import EnhancedRequestOptimizer, UserAgentPool, ProxyPool
    except ImportError:
        EnhancedRequestOptimizer = None
        UserAgentPool = None
        ProxyPool = None


class RequestOptimizer:
    """
    请求优化器（旧版本，保持向后兼容）
    推荐使用 anti_spider.EnhancedRequestOptimizer 获得更多功能
    """
    def __init__(self, delay_range: tuple = (1, 3), proxies: List[str] = None, logger: CtripSpiderLogger = None):
        self.delay_range = delay_range
        self.proxies = proxies if proxies is not None else []
        self.logger = logger or CtripSpiderLogger("RequestOptimizer", "logs")
        self.request_count = 0

    def set_delay(self):
        """设置随机延迟以防止被封禁"""
        delay = random.uniform(*self.delay_range)
        self.request_count += 1
        self.logger.log_request(f"Delay request #{self.request_count}", 200, delay, "SLEEP")
        time.sleep(delay)

    def get_random_proxy(self):
        """获取随机代理"""
        if self.proxies:
            proxy = random.choice(self.proxies)
            self.logger.info(f"Selected random proxy: {proxy}")
            return proxy
        else:
            self.logger.warning("No proxies available, returning None")
            return None

    def log_delay(self):
        """日志延迟信息"""
        delay = random.uniform(*self.delay_range)
        self.request_count += 1
        self.logger.info(f"Waiting for {delay:.2f} seconds before the next request (Request #{self.request_count})")
        time.sleep(delay)

# 示例用法
if __name__ == "__main__":
    # 初始化 CtripSpiderLogger
    spider_logger = CtripSpiderLogger("RequestOptimizerTest", "logs")
    # 初始化 RequestOptimizer，设置延迟范围和代理列表
    proxies_list = [
        "http://proxy1.com:8080",
        "http://proxy2.com:8080",
        "http://proxy3.com:8080"
    ]

    request_optimizer = RequestOptimizer(delay_range=(2, 5), proxies=proxies_list, logger=spider_logger)

    # 在爬虫逻辑中使用
    for i in range(5):
        request_optimizer.log_delay()  # 添加延迟
        proxy = request_optimizer.get_random_proxy()  # 获取代理
        spider_logger.info(f"Using proxy: {proxy}")  # 在实际请求中使用代理
        # 这里可以放置实际请求的代码

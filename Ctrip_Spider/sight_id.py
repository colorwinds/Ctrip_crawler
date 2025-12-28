import requests
import json
import time
import os
from typing import Tuple, Optional, List

# 处理相对导入和绝对导入
try:
    from .log import CtripSpiderLogger
    from .anti_spider import EnhancedRequestOptimizer
except ImportError:
    # 直接运行时使用绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Ctrip_Spider.log import CtripSpiderLogger
    from Ctrip_Spider.anti_spider import EnhancedRequestOptimizer


class SightId:
    """景点ID搜索器，用于根据关键词搜索景点ID"""

    def __init__(
        self,
        delay_range: Tuple[float, float] = (1, 3),
        proxies: List[str] = None,
        use_proxy: bool = False,
        use_user_agent_rotation: bool = True,
        logger: CtripSpiderLogger = None
    ):
        """初始化景点ID搜索器

        Args:
            delay_range: 延迟范围
            proxies: 代理列表
            use_proxy: 是否使用代理
            use_user_agent_rotation: 是否使用User-Agent轮换
            logger: 日志记录器实例
        """
        self.delay_range = delay_range
        self.search_url = "https://m.ctrip.com/restapi/soa2/26872/search"
        self.base_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.logger = logger or CtripSpiderLogger("SightId", "logs")
        
        # 初始化增强的请求优化器
        self.optimizer = EnhancedRequestOptimizer(
            delay_range=delay_range,
            proxies=proxies,
            use_proxy=use_proxy,
            use_user_agent_rotation=use_user_agent_rotation,
            rotation_mode='random',
            logger=self.logger
        )

    def search_sight_id(self, keyword: str) -> Optional[str]:
        """根据关键词搜索景点ID

        Args:
            keyword: 景点关键词

        Returns:
            str: 景点ID，未找到时返回None
        """
        self.logger.info(f"开始搜索景点ID，关键词: {keyword}")
        try:
            codedata = {
                "action": "online",
                "source": "globalonline",
                "keyword": keyword,
                "pagenum": 1,
                "pagesize": 10
            }

            start_time = time.time()
            # 使用增强的请求优化器发送请求
            headers = self.optimizer.get_headers(self.base_headers)
            proxies = self.optimizer.get_proxy_dict()
            
            response = requests.post(
                self.search_url,
                data=json.dumps(codedata),
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            response.raise_for_status()
            data_dict = response.json()
            end_time = time.time()
            response_time = end_time - start_time

            # 记录请求信息
            self.logger.log_request(self.search_url, response.status_code, response_time, "POST")
            
            # 如果使用代理，更新代理状态
            if proxies and self.optimizer.use_proxy:
                proxy_url = proxies.get('http') or proxies.get('https')
                if response.status_code == 200:
                    self.optimizer.proxy_pool.mark_success(proxy_url)
                else:
                    self.optimizer.proxy_pool.mark_fail(proxy_url)

            if data_dict.get('data') and isinstance(data_dict['data'], list) and len(data_dict['data']) > 0:
                sight_id = data_dict['data'][0].get('id')
                self.logger.info(f"成功获取景点ID: {sight_id}，关键词: {keyword}")
                self.logger.log_data_extraction(1, "sight_id")
                return sight_id
            else:
                self.logger.warning(f"未找到与关键词 '{keyword}' 匹配的景点ID")
                return None

        except Exception as e:
            self.logger.log_error(f"搜索景点ID时发生错误: {e}", self.search_url, "POST")
            import traceback
            self.logger.error(traceback.format_exc())
            return None


if __name__ == "__main__":
    # 创建日志记录器
    logger = CtripSpiderLogger("SightIdMain", "logs")
    # 创建爬虫实例
    crawler = SightId(delay_range=(1, 2), logger=logger)  # 设置较短的延迟以便快速测试
    
    # 测试景点关键词
    test_keyword = "黄鹤楼"
    logger.info(f"开始测试评论爬取功能，搜索关键词: {test_keyword}")
    
    # 测试景点ID搜索
    sight_id = crawler.search_sight_id(test_keyword)
    if sight_id:
        logger.info(f"✓ 成功获取景点ID: {sight_id}")
    else:
        logger.error("✗ 无法获取景点ID，测试终止")
        exit(1)
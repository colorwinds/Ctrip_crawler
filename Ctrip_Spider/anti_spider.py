"""
反爬虫策略模块
提供User-Agent轮换、代理池管理、请求优化等功能
"""
import random
import time
import requests
from typing import List, Dict, Optional, Tuple
from collections import deque
from datetime import datetime, timedelta

# 处理相对导入和绝对导入
try:
    from .log import CtripSpiderLogger
except ImportError:
    # 直接运行时使用绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Ctrip_Spider.log import CtripSpiderLogger


class UserAgentPool:
    """User-Agent池管理类"""
    
    # 常见的User-Agent列表（包含不同浏览器和操作系统）
    DEFAULT_USER_AGENTS = [
        # Chrome on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        
        # Chrome on macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        
        # Firefox on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
        
        # Firefox on macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
        
        # Edge on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        
        # Safari on macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        
        # Chrome on Linux
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        
        # Mobile User-Agents
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    ]
    
    def __init__(self, user_agents: List[str] = None):
        """
        初始化User-Agent池
        
        Args:
            user_agents: 自定义User-Agent列表，如果为None则使用默认列表
        """
        self.user_agents = user_agents if user_agents else self.DEFAULT_USER_AGENTS.copy()
        self.current_index = 0
        self.usage_count = {ua: 0 for ua in self.user_agents}
    
    def get_random(self) -> str:
        """随机获取一个User-Agent"""
        ua = random.choice(self.user_agents)
        self.usage_count[ua] += 1
        return ua
    
    def get_round_robin(self) -> str:
        """轮询获取User-Agent"""
        ua = self.user_agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.user_agents)
        self.usage_count[ua] += 1
        return ua
    
    def add(self, user_agent: str):
        """添加新的User-Agent"""
        if user_agent not in self.user_agents:
            self.user_agents.append(user_agent)
            self.usage_count[user_agent] = 0
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        return {
            'total': len(self.user_agents),
            'usage_count': self.usage_count.copy()
        }


class ProxyPool:
    """代理池管理类"""
    
    def __init__(self, proxies: List[str] = None, logger: CtripSpiderLogger = None):
        """
        初始化代理池
        
        Args:
            proxies: 代理列表，格式: ['http://user:pass@host:port', ...]
            logger: 日志记录器
        """
        self.logger = logger or CtripSpiderLogger("ProxyPool", "logs")
        self.proxies = []
        self.proxy_stats = {}  # 代理统计信息
        self.failed_proxies = set()  # 失败的代理
        self.proxy_check_timeout = 5  # 代理检查超时时间
        
        if proxies:
            for proxy in proxies:
                self.add_proxy(proxy)
    
    def add_proxy(self, proxy: str):
        """添加代理到池中"""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            self.proxy_stats[proxy] = {
                'success_count': 0,
                'fail_count': 0,
                'last_used': None,
                'last_success': None,
                'last_fail': None,
                'is_active': True
            }
            self.logger.info(f"添加代理: {proxy}")
    
    def remove_proxy(self, proxy: str):
        """从池中移除代理"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            if proxy in self.proxy_stats:
                del self.proxy_stats[proxy]
            self.failed_proxies.discard(proxy)
            self.logger.info(f"移除代理: {proxy}")
    
    def check_proxy(self, proxy: str, test_url: str = "https://www.baidu.com", timeout: int = 5) -> bool:
        """
        检查代理是否可用
        
        Args:
            proxy: 代理地址
            test_url: 测试URL
            timeout: 超时时间
            
        Returns:
            bool: 代理是否可用
        """
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                self.logger.debug(f"代理 {proxy} 检查通过")
                return True
            else:
                self.logger.warning(f"代理 {proxy} 检查失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            self.logger.debug(f"代理 {proxy} 检查失败: {e}")
            return False
    
    def get_random_proxy(self) -> Optional[str]:
        """随机获取一个可用代理"""
        active_proxies = [p for p in self.proxies if self.proxy_stats[p]['is_active']]
        if not active_proxies:
            self.logger.warning("没有可用的代理")
            return None
        
        proxy = random.choice(active_proxies)
        self.proxy_stats[proxy]['last_used'] = datetime.now()
        return proxy
    
    def get_round_robin_proxy(self) -> Optional[str]:
        """轮询获取代理"""
        active_proxies = [p for p in self.proxies if self.proxy_stats[p]['is_active']]
        if not active_proxies:
            return None
        
        # 按使用次数排序，优先使用使用次数少的
        active_proxies.sort(key=lambda p: self.proxy_stats[p]['success_count'])
        proxy = active_proxies[0]
        self.proxy_stats[proxy]['last_used'] = datetime.now()
        return proxy
    
    def mark_success(self, proxy: str):
        """标记代理使用成功"""
        if proxy in self.proxy_stats:
            self.proxy_stats[proxy]['success_count'] += 1
            self.proxy_stats[proxy]['last_success'] = datetime.now()
            self.proxy_stats[proxy]['is_active'] = True
            self.failed_proxies.discard(proxy)
    
    def mark_fail(self, proxy: str, max_fails: int = 3):
        """标记代理使用失败"""
        if proxy in self.proxy_stats:
            self.proxy_stats[proxy]['fail_count'] += 1
            self.proxy_stats[proxy]['last_fail'] = datetime.now()
            
            # 如果失败次数超过阈值，标记为不活跃
            if self.proxy_stats[proxy]['fail_count'] >= max_fails:
                self.proxy_stats[proxy]['is_active'] = False
                self.failed_proxies.add(proxy)
                self.logger.warning(f"代理 {proxy} 失败次数过多，已标记为不活跃")
    
    def check_all_proxies(self, test_url: str = "https://www.baidu.com"):
        """检查所有代理的可用性"""
        self.logger.info(f"开始检查 {len(self.proxies)} 个代理的可用性...")
        for proxy in self.proxies:
            is_valid = self.check_proxy(proxy, test_url)
            if is_valid:
                self.mark_success(proxy)
            else:
                self.mark_fail(proxy, max_fails=1)
        
        active_count = sum(1 for p in self.proxies if self.proxy_stats[p]['is_active'])
        self.logger.info(f"代理检查完成，可用代理: {active_count}/{len(self.proxies)}")
    
    def get_stats(self) -> Dict:
        """获取代理池统计信息"""
        active_count = sum(1 for p in self.proxies if self.proxy_stats[p]['is_active'])
        return {
            'total': len(self.proxies),
            'active': active_count,
            'failed': len(self.failed_proxies),
            'stats': self.proxy_stats.copy()
        }


class EnhancedRequestOptimizer:
    """增强的请求优化器，集成User-Agent轮换和代理池管理"""
    
    def __init__(
        self,
        delay_range: Tuple[float, float] = (1, 3),
        user_agents: List[str] = None,
        proxies: List[str] = None,
        use_proxy: bool = False,
        use_user_agent_rotation: bool = True,
        rotation_mode: str = 'random',  # 'random' or 'round_robin'
        logger: CtripSpiderLogger = None
    ):
        """
        初始化增强的请求优化器
        
        Args:
            delay_range: 延迟范围（秒）
            user_agents: 自定义User-Agent列表
            proxies: 代理列表
            use_proxy: 是否使用代理
            use_user_agent_rotation: 是否使用User-Agent轮换
            rotation_mode: 轮换模式，'random'或'round_robin'
            logger: 日志记录器
        """
        self.delay_range = delay_range
        self.use_proxy = use_proxy
        self.use_user_agent_rotation = use_user_agent_rotation
        self.rotation_mode = rotation_mode
        self.logger = logger or CtripSpiderLogger("EnhancedRequestOptimizer", "logs")
        self.request_count = 0
        
        # 初始化User-Agent池
        self.ua_pool = UserAgentPool(user_agents)
        
        # 初始化代理池
        self.proxy_pool = ProxyPool(proxies, logger=self.logger)
        
        # 如果启用代理但没有提供代理，给出警告
        if use_proxy and not proxies:
            self.logger.warning("已启用代理但未提供代理列表，代理功能将不可用")
            self.use_proxy = False
    
    def get_headers(self, base_headers: Dict = None) -> Dict:
        """
        获取请求头，包含随机User-Agent
        
        Args:
            base_headers: 基础请求头
            
        Returns:
            dict: 完整的请求头
        """
        headers = base_headers.copy() if base_headers else {}
        
        if self.use_user_agent_rotation:
            if self.rotation_mode == 'random':
                ua = self.ua_pool.get_random()
            else:
                ua = self.ua_pool.get_round_robin()
            headers['User-Agent'] = ua
            self.logger.debug(f"使用User-Agent: {ua[:50]}...")
        
        return headers
    
    def get_proxy_dict(self) -> Optional[Dict]:
        """
        获取代理字典
        
        Returns:
            dict: 代理字典，格式: {'http': '...', 'https': '...'}
        """
        if not self.use_proxy:
            return None
        
        proxy = None
        if self.rotation_mode == 'random':
            proxy = self.proxy_pool.get_random_proxy()
        else:
            proxy = self.proxy_pool.get_round_robin_proxy()
        
        if proxy:
            self.logger.debug(f"使用代理: {proxy}")
            return {
                'http': proxy,
                'https': proxy
            }
        else:
            self.logger.warning("无法获取可用代理")
            return None
    
    def set_delay(self):
        """设置随机延迟"""
        delay = random.uniform(*self.delay_range)
        self.request_count += 1
        self.logger.debug(f"延迟 {delay:.2f} 秒 (请求 #{self.request_count})")
        time.sleep(delay)
    
    def make_request(
        self,
        method: str,
        url: str,
        base_headers: Dict = None,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        发送HTTP请求，自动应用反爬虫策略
        
        Args:
            method: HTTP方法 ('GET', 'POST', etc.)
            base_headers: 基础请求头
            **kwargs: requests的其他参数
            
        Returns:
            requests.Response: 响应对象，失败时返回None
        """
        # 应用延迟
        self.set_delay()
        
        # 获取请求头
        headers = self.get_headers(base_headers)
        
        # 获取代理
        proxies = self.get_proxy_dict()
        
        # 准备请求参数
        request_kwargs = {
            'headers': headers,
            'timeout': kwargs.get('timeout', 10)
        }
        
        if proxies:
            request_kwargs['proxies'] = proxies
        
        # 添加其他参数
        for key in ['json', 'data', 'params', 'files']:
            if key in kwargs:
                request_kwargs[key] = kwargs[key]
        
        try:
            # 发送请求
            response = requests.request(method, url, **request_kwargs)
            
            # 如果使用代理，记录代理状态
            if proxies and self.use_proxy:
                proxy_url = proxies.get('http') or proxies.get('https')
                if response.status_code == 200:
                    self.proxy_pool.mark_success(proxy_url)
                else:
                    self.proxy_pool.mark_fail(proxy_url)
            
            return response
            
        except requests.exceptions.ProxyError as e:
            if proxies:
                proxy_url = proxies.get('http') or proxies.get('https')
                self.proxy_pool.mark_fail(proxy_url)
                self.logger.error(f"代理错误: {e}")
            return None
        except Exception as e:
            self.logger.error(f"请求错误: {e}")
            return None
    
    def check_proxies(self, test_url: str = "https://www.baidu.com"):
        """检查所有代理的可用性"""
        self.proxy_pool.check_all_proxies(test_url)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'request_count': self.request_count,
            'user_agent_stats': self.ua_pool.get_stats(),
            'proxy_stats': self.proxy_pool.get_stats()
        }


# 使用示例
if __name__ == "__main__":
    from .log import CtripSpiderLogger
    
    logger = CtripSpiderLogger("AntiSpiderTest", "logs")
    
    # 创建优化器实例
    optimizer = EnhancedRequestOptimizer(
        delay_range=(1, 2),
        proxies=None,  # 可以添加代理列表: ['http://proxy1:port', ...]
        use_proxy=False,  # 如果没有代理，设置为False
        use_user_agent_rotation=True,
        rotation_mode='random',
        logger=logger
    )
    
    # 测试User-Agent轮换
    logger.info("测试User-Agent轮换:")
    for i in range(5):
        headers = optimizer.get_headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        logger.info(f"请求 {i+1}: User-Agent = {headers['User-Agent'][:60]}...")
    
    # 获取统计信息
    stats = optimizer.get_stats()
    logger.info(f"\n统计信息:\n{stats}")


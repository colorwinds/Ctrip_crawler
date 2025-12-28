"""
反爬虫策略使用示例
演示如何使用增强的反爬虫功能
"""
from log import CtripSpiderLogger
from anti_spider import EnhancedRequestOptimizer, UserAgentPool, ProxyPool
from sight_id import SightId
from sight_list import CtripAttractionScraper
from sight_comments import CtripCommentSpider
from sight_detail import AttractionDetailFetcher


def example_user_agent_rotation():
    """示例1: User-Agent轮换"""
    print("=" * 60)
    print("示例1: User-Agent轮换")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleUA", "logs")
    
    # 创建优化器，启用User-Agent轮换
    optimizer = EnhancedRequestOptimizer(
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        rotation_mode='random',  # 或 'round_robin'
        logger=logger
    )
    
    # 获取多个不同的User-Agent
    print("\n获取5个不同的User-Agent:")
    for i in range(5):
        headers = optimizer.get_headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        print(f"{i+1}. {headers['User-Agent'][:80]}...")
    
    # 查看统计信息
    stats = optimizer.get_stats()
    print(f"\nUser-Agent池统计: 总数={stats['user_agent_stats']['total']}")


def example_proxy_pool():
    """示例2: 代理池管理"""
    print("\n" + "=" * 60)
    print("示例2: 代理池管理")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleProxy", "logs")
    
    # 注意：这里使用示例代理，实际使用时需要替换为真实代理
    example_proxies = [
        # 'http://proxy1.example.com:8080',
        # 'http://user:pass@proxy2.example.com:8080',
        # 'socks5://proxy3.example.com:1080',
    ]
    
    if not example_proxies:
        print("\n注意: 未配置代理，跳过代理测试")
        print("要使用代理功能，请在example_proxies列表中添加代理地址")
        return
    
    # 创建代理池
    proxy_pool = ProxyPool(proxies=example_proxies, logger=logger)
    
    # 检查所有代理的可用性
    print("\n检查代理可用性...")
    proxy_pool.check_all_proxies()
    
    # 获取代理统计信息
    stats = proxy_pool.get_stats()
    print(f"\n代理池统计:")
    print(f"  总数: {stats['total']}")
    print(f"  可用: {stats['active']}")
    print(f"  失败: {stats['failed']}")


def example_sight_id_with_anti_spider():
    """示例3: 使用反爬虫策略搜索景点ID"""
    print("\n" + "=" * 60)
    print("示例3: 使用反爬虫策略搜索景点ID")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleSightId", "logs")
    
    # 创建景点ID搜索器，启用User-Agent轮换
    sight_id_searcher = SightId(
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        use_proxy=False,  # 如果有代理，可以设置为True
        logger=logger
    )
    
    # 搜索景点ID
    keyword = "黄鹤楼"
    print(f"\n搜索关键词: {keyword}")
    sight_id = sight_id_searcher.search_sight_id(keyword)
    
    if sight_id:
        print(f"✓ 成功获取景点ID: {sight_id}")
    else:
        print("✗ 未找到景点ID")


def example_comments_with_anti_spider():
    """示例4: 使用反爬虫策略爬取评论"""
    print("\n" + "=" * 60)
    print("示例4: 使用反爬虫策略爬取评论")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleComments", "logs")
    
    # 创建评论爬虫，启用User-Agent轮换和延迟
    comment_spider = CtripCommentSpider(
        output_dir='./Datasets',
        delay_range=(1, 2),  # 每次请求延迟1-2秒
        use_user_agent_rotation=True,
        use_proxy=False,  # 如果有代理，可以设置为True
        logger=logger
    )
    
    # 爬取评论（只爬取2页作为示例）
    print("\n开始爬取评论...")
    success = comment_spider.crawl_comments(
        poi_id='76865',
        poi_name='星海广场',
        max_pages=2  # 只爬取2页作为示例
    )
    
    if success:
        print("✓ 评论爬取成功")
    else:
        print("✗ 评论爬取失败")


def example_attraction_list_with_anti_spider():
    """示例5: 使用反爬虫策略获取景点列表"""
    print("\n" + "=" * 60)
    print("示例5: 使用反爬虫策略获取景点列表")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleAttractionList", "logs")
    
    # 创建景点列表爬虫，启用User-Agent轮换
    scraper = CtripAttractionScraper(
        timeout=10,
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        use_proxy=False,
        logger=logger
    )
    
    # 获取景点列表（只获取1页作为示例）
    print("\n获取景点列表...")
    attractions = scraper.get_attractions_list(district_id=9, page=1, count=5)
    
    if attractions:
        print(f"✓ 成功获取 {len(attractions)} 个景点")
        for i, attr in enumerate(attractions[:3], 1):  # 只显示前3个
            print(f"  {i}. {attr['name']} - 评分: {attr['rating']}")
    else:
        print("✗ 未获取到景点数据")


def example_optimizer_stats():
    """示例6: 查看优化器统计信息"""
    print("\n" + "=" * 60)
    print("示例6: 查看优化器统计信息")
    print("=" * 60)
    
    logger = CtripSpiderLogger("ExampleStats", "logs")
    
    # 创建优化器
    optimizer = EnhancedRequestOptimizer(
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        logger=logger
    )
    
    # 模拟多次请求
    print("\n模拟10次请求...")
    for i in range(10):
        optimizer.set_delay()
        headers = optimizer.get_headers()
    
    # 获取统计信息
    stats = optimizer.get_stats()
    print(f"\n优化器统计信息:")
    print(f"  总请求数: {stats['request_count']}")
    print(f"  User-Agent总数: {stats['user_agent_stats']['total']}")
    print(f"  代理总数: {stats['proxy_stats']['total']}")
    print(f"  可用代理: {stats['proxy_stats']['active']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("反爬虫策略使用示例")
    print("=" * 60)
    
    # 运行各个示例
    example_user_agent_rotation()
    example_proxy_pool()
    example_sight_id_with_anti_spider()
    example_attraction_list_with_anti_spider()
    example_comments_with_anti_spider()
    example_optimizer_stats()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


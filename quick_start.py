"""
快速开始示例 - 最简单的使用方式
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Ctrip_Spider.log import CtripSpiderLogger
from Ctrip_Spider.sight_id import SightId
from Ctrip_Spider.sight_comments import CtripCommentSpider


def quick_example():
    """快速示例：搜索景点并爬取评论"""
    
    # 1. 创建日志记录器
    logger = CtripSpiderLogger("QuickStart", "logs")
    
    # 2. 搜索景点ID
    print("="*60)
    print("步骤1: 搜索景点ID")
    print("="*60)
    
    searcher = SightId(
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        logger=logger
    )
    
    # 输入：景点关键词
    keyword = "黄鹤楼"  # 可以修改为其他景点名称
    print(f"\n搜索关键词: {keyword}")
    
    sight_id = searcher.search_sight_id(keyword)
    
    if not sight_id:
        print("未找到景点ID，请尝试其他关键词")
        return
    
    print(f"✓ 找到景点ID: {sight_id}")
    
    # 3. 爬取评论
    print("\n" + "="*60)
    print("步骤2: 爬取评论")
    print("="*60)
    
    spider = CtripCommentSpider(
        output_dir='./Datasets',
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        logger=logger
    )
    
    # 输入：POI ID, 景点名称, 最大页数
    # 注意：这里需要POI ID，不是sight_id
    # 如果不知道POI ID，可以先运行 sight_list.py 获取
    poi_id = "76865"  # 示例：星海广场的POI ID
    poi_name = "星海广场"  # 景点名称
    max_pages = 2  # 爬取2页（可以修改为更多）
    
    print(f"\n景点: {poi_name}")
    print(f"POI ID: {poi_id}")
    print(f"爬取页数: {max_pages}")
    print("\n开始爬取...")
    
    success = spider.crawl_comments(
        poi_id=poi_id,
        poi_name=poi_name,
        max_pages=max_pages
    )
    
    if success:
        print(f"\n✓ 爬取完成！")
        print(f"数据保存在: ./Datasets/{poi_id}_{poi_name}.csv")
    else:
        print("\n✗ 爬取失败，请查看日志文件")


if __name__ == "__main__":
    print("\n携程数据爬虫 - 快速开始示例\n")
    print("提示: 请确保已安装依赖: pip install requests beautifulsoup4\n")
    
    # 创建必要的目录
    os.makedirs('./Datasets', exist_ok=True)
    os.makedirs('./logs', exist_ok=True)
    
    try:
        quick_example()
        print("\n" + "="*60)
        print("完成！")
        print("="*60)
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()


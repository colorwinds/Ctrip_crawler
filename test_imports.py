"""
测试导入是否正常
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("测试导入...")
    
    # 测试导入各个模块
    from Ctrip_Spider.log import CtripSpiderLogger
    print("✓ log 模块导入成功")
    
    from Ctrip_Spider.anti_spider import EnhancedRequestOptimizer
    print("✓ anti_spider 模块导入成功")
    
    from Ctrip_Spider.sight_id import SightId
    print("✓ sight_id 模块导入成功")
    
    from Ctrip_Spider.sight_list import CtripAttractionScraper
    print("✓ sight_list 模块导入成功")
    
    from Ctrip_Spider.sight_detail import AttractionDetailFetcher
    print("✓ sight_detail 模块导入成功")
    
    from Ctrip_Spider.sight_comments import CtripCommentSpider
    print("✓ sight_comments 模块导入成功")
    
    print("\n所有模块导入成功！")
    
except ImportError as e:
    print(f"\n✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


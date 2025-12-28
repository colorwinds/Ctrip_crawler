"""
携程数据爬虫主程序示例 / Ctrip Data Spider Main Example

本文件包含完整的使用示例和文档说明，演示如何使用各个模块进行数据爬取。
This file contains complete usage examples and documentation demonstrating how to use each module for data scraping.

🚀 快速开始 / Quick Start
-------------------------

1. 环境准备 / Prerequisites:
   - Python 3.7+
   - 安装依赖 / Install dependencies:
     pip install requests beautifulsoup4

2. 运行示例 / Run examples:
   python main_example.py

📝 输入参数说明 / Input Parameters
----------------------------------

示例1: 搜索景点ID / Example 1: Search Attraction ID
- keyword: 景点关键词（字符串）/ Attraction keyword (string)
  - 示例 / Examples: "黄鹤楼", "故宫", "天安门"

示例2: 获取景点列表 / Example 2: Get Attraction List
- district_id: 地区ID（整数）/ District ID (integer)
  - 常见地区ID / Common District IDs:
    9 = 北京 / Beijing
    2 = 上海 / Shanghai
    7 = 广州 / Guangzhou
    26 = 深圳 / Shenzhen
    14 = 杭州 / Hangzhou
    104 = 成都 / Chengdu
    6 = 南京 / Nanjing
- page: 页码（整数，默认1）/ Page number (integer, default 1)
- count: 每页数量（整数，默认20）/ Count per page (integer, default 20)

示例3: 获取景点详情 / Example 3: Get Attraction Details
- poi_id: 景点POI ID（整数）/ Attraction POI ID (integer)
  - 可以从景点列表中获取 / Can be obtained from attraction list

示例4: 爬取评论 / Example 4: Scrape Comments
- poi_id: 景点POI ID（字符串）/ Attraction POI ID (string)
- poi_name: 景点名称（字符串）/ Attraction name (string)
- max_pages: 最大爬取页数（整数，默认100）/ Max pages to scrape (integer, default 100)

示例5: 批量爬取 / Example 5: Batch Scraping
- poi_list: 景点列表（列表，每个元素为 [poi_id, poi_name]）/ Attraction list (list, each element is [poi_id, poi_name])
- max_pages: 每个景点最大爬取页数 / Max pages per attraction

📊 输出文件说明 / Output Files
-------------------------------

1. 景点列表 (JSON格式) / Attraction List (JSON):
   - 文件名 / File: attractions_list.json
   - 字段 / Fields: name, id, poi_id, rating, review_count, price, address, etc.

2. 评论数据 (CSV格式) / Comments (CSV):
   - 文件名 / File: {poi_id}_{景点名称}.csv
   - 位置 / Location: ./Datasets/
   - 字段 / Fields: 评论ID, 用户昵称, 总体评分, 评论内容, 发布时间, 有用数, 回复数, 
     出行类型, 用户所在地, 游玩时长, 图片数量, 图片链接列表, 景色评分, 趣味评分, 
     性价比评分, 推荐项目

3. 日志文件 / Log Files:
   - 位置 / Location: ./logs/
   - 格式 / Format: {模块名}_{日期}.log

⚙️ 配置参数 / Configuration
---------------------------

- delay_range: 请求延迟范围（秒）/ Request delay range (seconds)
  推荐值 / Recommended: (1, 3)
- use_user_agent_rotation: User-Agent轮换 / User-Agent rotation
  推荐值 / Recommended: True
- use_proxy: 是否使用代理 / Use proxy (optional)
  需要配置proxies列表 / Requires proxies list

⚠️ 注意事项 / Important Notes
-----------------------------

1. 遵守协议 / Compliance: 请遵守网站的robots.txt和使用协议
2. 合理频率 / Rate Limiting: 建议设置合理的延迟范围（1-3秒）
3. 数据使用 / Data Usage: 爬取的数据仅供学习研究使用
4. 错误处理 / Error Handling: 建议监控日志文件
5. 代理使用 / Proxy Usage: 如需使用代理，请确保代理可用性

🐛 常见问题 / Troubleshooting
------------------------------

Q1: 无法获取数据？/ Cannot retrieve data?
- 检查网络连接 / Check network connection
- 查看日志文件了解错误详情 / Review log files for error details
- 尝试增加延迟时间 / Try increasing delay time
- 检查是否被限制访问 / Check if access is restricted

Q2: 评论爬取失败？/ Comment scraping failed?
- 确认POI ID是否正确 / Verify POI ID is correct
- 检查景点是否有评论 / Check if the attraction has comments
- 查看日志文件了解具体错误 / Review log files for specific errors

Q3: 如何获取更多地区ID？/ How to get more district IDs?
- 使用浏览器开发者工具查看携程网站的网络请求 / Use browser developer tools
- 或使用 sight_list.py 尝试不同的district_id / Or try different district_id values
"""
import os
import sys

# 添加项目路径到sys.path / Add project path to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Ctrip_Spider.log import CtripSpiderLogger
from Ctrip_Spider.sight_id import SightId
from Ctrip_Spider.sight_list import CtripAttractionScraper
from Ctrip_Spider.sight_detail import AttractionDetailFetcher
from Ctrip_Spider.sight_comments import CtripCommentSpider


# 常见地区ID参考 / Common District IDs Reference
COMMON_DISTRICT_IDS = {
    9: "北京 / Beijing",
    2: "上海 / Shanghai",
    7: "广州 / Guangzhou",
    26: "深圳 / Shenzhen",
    14: "杭州 / Hangzhou",
    104: "成都 / Chengdu",
    6: "南京 / Nanjing",
}


def example_1_search_sight_id():
    """
    示例1: 根据关键词搜索景点ID / Example 1: Search Attraction ID by Keyword
    
    输入参数 / Input Parameters:
        keyword: 景点关键词（字符串）/ Attraction keyword (string)
        示例 / Examples: "黄鹤楼", "故宫", "天安门"
    
    返回 / Returns:
        dict: {关键词: 景点ID} / {keyword: sight_id}
    """
    print("\n" + "="*60)
    print("示例1: 搜索景点ID / Example 1: Search Attraction ID")
    print("="*60)
    
    logger = CtripSpiderLogger("SearchSightId", "logs")
    
    # 创建景点ID搜索器 / Create attraction ID searcher
    sight_id_searcher = SightId(
        delay_range=(1, 2),  # 请求延迟范围（秒）/ Request delay range (seconds)
        use_user_agent_rotation=True,  # 启用User-Agent轮换 / Enable User-Agent rotation
        logger=logger
    )
    
    # 搜索关键词列表 / Search keyword list
    keywords = ["黄鹤楼", "故宫", "天安门"]
    
    print("\n开始搜索景点ID... / Starting to search attraction IDs...")
    results = {}
    
    for keyword in keywords:
        print(f"\n搜索关键词 / Searching keyword: {keyword}")
        sight_id = sight_id_searcher.search_sight_id(keyword)
        
        if sight_id:
            results[keyword] = sight_id
            print(f"  ✓ 找到景点ID / Found attraction ID: {sight_id}")
        else:
            print(f"  ✗ 未找到景点 / Attraction not found")
    
    return results


def example_2_get_attraction_list():
    """
    示例2: 获取景点列表 / Example 2: Get Attraction List
    
    输入参数 / Input Parameters:
        district_id: 地区ID（整数）/ District ID (integer)
            - 9 = 北京 / Beijing
            - 2 = 上海 / Shanghai
            - 7 = 广州 / Guangzhou
            - 更多地区ID见 COMMON_DISTRICT_IDS / See COMMON_DISTRICT_IDS for more
        pages: 页数（整数）/ Number of pages (integer)
        count_per_page: 每页数量（整数）/ Count per page (integer)
    
    返回 / Returns:
        list: 景点列表 / List of attractions
    """
    print("\n" + "="*60)
    print("示例2: 获取景点列表 / Example 2: Get Attraction List")
    print("="*60)
    
    logger = CtripSpiderLogger("GetAttractionList", "logs")
    
    # 创建景点列表爬取器 / Create attraction list scraper
    scraper = CtripAttractionScraper(
        timeout=10,
        delay_range=(1, 2),  # 请求延迟范围（秒）/ Request delay range (seconds)
        use_user_agent_rotation=True,  # 启用User-Agent轮换 / Enable User-Agent rotation
        logger=logger
    )
    
    # 地区ID说明 / District ID notes:
    # 9 = 北京 / Beijing
    # 2 = 上海 / Shanghai
    # 7 = 广州 / Guangzhou
    # 可以根据需要修改 / Can be modified as needed
    district_id = 9  # 北京 / Beijing
    pages = 2  # 获取2页数据 / Get 2 pages of data
    count_per_page = 5  # 每页5个景点 / 5 attractions per page
    
    print(f"\n获取地区ID {district_id} 的景点列表... / Getting attraction list for district ID {district_id}...")
    print(f"页数 / Pages: {pages}, 每页数量 / Count per page: {count_per_page}")
    
    attractions = scraper.get_attractions_with_pagination(
        district_id=district_id,
        pages=pages,
        count_per_page=count_per_page
    )
    
    if attractions:
        print(f"\n✓ 成功获取 {len(attractions)} 个景点 / Successfully retrieved {len(attractions)} attractions")
        print("\n景点列表 / Attraction List:")
        for i, attr in enumerate(attractions[:10], 1):  # 显示前10个 / Show first 10
            print(f"\n{i}. {attr['name']}")
            print(f"   ID: {attr['id']}")
            print(f"   评分 / Rating: {attr['rating']} (基于{attr['review_count']}条评论 / based on {attr['review_count']} reviews)")
            print(f"   价格 / Price: {attr.get('price', 0)}元")
            print(f"   地址 / Address: {attr.get('address', '未知 / Unknown')}")
        
        # 保存到JSON文件 / Save to JSON file
        output_file = './attractions_list.json'
        scraper.save_to_json(attractions, output_file)
        print(f"\n✓ 数据已保存到 / Data saved to: {output_file}")
        
        return attractions
    else:
        print("\n✗ 未获取到景点数据 / No attraction data retrieved")
        return []


def example_3_get_attraction_detail():
    """
    示例3: 获取景点详细信息 / Example 3: Get Attraction Details
    
    输入参数 / Input Parameters:
        poi_id: 景点POI ID（整数）/ Attraction POI ID (integer)
        - 可以从景点列表中获取 / Can be obtained from attraction list
    
    返回 / Returns:
        list: 景点详情列表 / List of attraction details
    """
    print("\n" + "="*60)
    print("示例3: 获取景点详细信息 / Example 3: Get Attraction Details")
    print("="*60)
    
    logger = CtripSpiderLogger("GetAttractionDetail", "logs")
    
    # 创建景点详情获取器 / Create attraction detail fetcher
    detail_fetcher = AttractionDetailFetcher(
        delay_range=(1, 2),  # 请求延迟范围（秒）/ Request delay range (seconds)
        use_user_agent_rotation=True,  # 启用User-Agent轮换 / Enable User-Agent rotation
        logger=logger
    )
    
    # 景点POI ID列表（可以从景点列表中获取）/ Attraction POI ID list (can be obtained from attraction list)
    poi_ids = [87211, 76865]  # 示例POI ID / Example POI IDs
    
    print("\n开始获取景点详情... / Starting to fetch attraction details...")
    details = []
    
    for poi_id in poi_ids:
        print(f"\n获取POI ID / Fetching POI ID: {poi_id}")
        detail = detail_fetcher.get_detail(poi_id)
        
        if detail.get('success'):
            details.append(detail)
            print(f"  ✓ 成功获取详情 / Successfully fetched details")
            print(f"  景点名称 / Attraction Name: {detail.get('poi_name', '未知 / Unknown')}")
            print(f"  英文名 / English Name: {detail.get('english_name', '未知 / Unknown')}")
            print(f"  所在地区 / District: {detail.get('district', '未知 / Unknown')}")
            print(f"  门票价格 / Ticket Price: {detail.get('ticket_price', '未知 / Unknown')}")
            print(f"  联系电话 / Telephone: {', '.join(detail.get('telephone', []))}")
        else:
            print(f"  ✗ 获取失败 / Failed to fetch: {detail.get('error_message', '未知错误 / Unknown error')}")
    
    return details


def example_4_crawl_comments():
    """
    示例4: 爬取景点评论 / Example 4: Scrape Attraction Comments
    
    输入参数 / Input Parameters:
        poi_id: 景点POI ID（字符串）/ Attraction POI ID (string)
        poi_name: 景点名称（字符串）/ Attraction name (string)
        max_pages: 最大爬取页数（整数）/ Maximum pages to scrape (integer)
    
    返回 / Returns:
        dict: 爬取结果 / Scraping results
    """
    print("\n" + "="*60)
    print("示例4: 爬取景点评论 / Example 4: Scrape Attraction Comments")
    print("="*60)
    
    logger = CtripSpiderLogger("CrawlComments", "logs")
    
    # 创建评论爬虫 / Create comment spider
    comment_spider = CtripCommentSpider(
        output_dir='./Datasets',  # 输出目录 / Output directory
        delay_range=(1, 2),  # 每次请求延迟1-2秒 / Delay 1-2 seconds per request
        use_user_agent_rotation=True,  # 启用User-Agent轮换 / Enable User-Agent rotation
        logger=logger
    )
    
    # 景点列表：格式为 [poi_id, poi_name] / Attraction list: format [poi_id, poi_name]
    pois = [
        ['76865', '星海广场'],
        ['75628', '棒棰岛'],
    ]
    
    print("\n开始爬取评论... / Starting to scrape comments...")
    print(f"景点数量 / Number of attractions: {len(pois)}")
    print(f"输出目录 / Output directory: {comment_spider.output_dir}")
    
    # 批量爬取评论 / Batch scrape comments
    results = comment_spider.crawl_multiple_pois(
        poi_list=pois,
        max_pages=3  # 每个景点爬取3页（可根据需要调整）/ Scrape 3 pages per attraction (adjustable)
    )
    
    # 显示结果 / Display results
    print("\n爬取结果汇总 / Scraping Results Summary:")
    for poi, success in results.items():
        status = "✓ 成功 / Success" if success else "✗ 失败 / Failed"
        print(f"  {poi}: {status}")
    
    return results


def example_5_complete_workflow():
    """
    示例5: 完整工作流程 - 从搜索到爬取评论 / Example 5: Complete Workflow - From Search to Comment Scraping
    
    演示完整的数据爬取流程：
    1. 搜索景点ID
    2. 获取景点列表
    3. 获取景点详情
    4. 爬取评论
    
    Demonstrates complete data scraping workflow:
    1. Search attraction ID
    2. Get attraction list
    3. Get attraction details
    4. Scrape comments
    """
    print("\n" + "="*60)
    print("示例5: 完整工作流程 / Example 5: Complete Workflow")
    print("="*60)
    
    logger = CtripSpiderLogger("CompleteWorkflow", "logs")
    
    # 步骤1: 搜索景点ID / Step 1: Search Attraction ID
    print("\n[步骤1 / Step 1] 搜索景点ID / Searching Attraction ID...")
    keyword = "黄鹤楼"
    sight_id_searcher = SightId(
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        logger=logger
    )
    sight_id = sight_id_searcher.search_sight_id(keyword)
    
    if not sight_id:
        print(f"未找到关键词 '{keyword}' 对应的景点ID，终止流程 / No attraction ID found for keyword '{keyword}', terminating workflow")
        return
    
    print(f"✓ 找到景点ID / Found attraction ID: {sight_id}")
    
    # 步骤2: 获取景点列表（可选，如果需要POI ID）/ Step 2: Get Attraction List (optional, if POI ID needed)
    print("\n[步骤2 / Step 2] 获取景点列表 / Getting Attraction List...")
    scraper = CtripAttractionScraper(
        timeout=10,
        delay_range=(1, 2),
        use_user_agent_rotation=True,
        logger=logger
    )
    attractions = scraper.get_attractions_list(district_id=9, page=1, count=10)
    
    if attractions:
        print(f"✓ 获取到 {len(attractions)} 个景点 / Retrieved {len(attractions)} attractions")
        # 找到匹配的景点 / Find matching attraction
        target_attraction = None
        for attr in attractions:
            if attr.get('id') == sight_id:
                target_attraction = attr
                break
        
        if target_attraction:
            poi_id = target_attraction.get('poi_id')
            poi_name = target_attraction.get('name')
            print(f"✓ 找到目标景点 / Found target attraction: {poi_name} (POI ID: {poi_id})")
            
            # 步骤3: 获取景点详情 / Step 3: Get Attraction Details
            print("\n[步骤3 / Step 3] 获取景点详情 / Getting Attraction Details...")
            detail_fetcher = AttractionDetailFetcher(
                delay_range=(1, 2),
                use_user_agent_rotation=True,
                logger=logger
            )
            detail = detail_fetcher.get_detail(poi_id)
            
            if detail.get('success'):
                print(f"✓ 成功获取详情 / Successfully fetched details")
                print(f"  描述 / Description: {detail.get('description', '')[:100]}...")
            
            # 步骤4: 爬取评论 / Step 4: Scrape Comments
            print("\n[步骤4 / Step 4] 爬取评论 / Scraping Comments...")
            comment_spider = CtripCommentSpider(
                output_dir='./Datasets',
                delay_range=(1, 2),
                use_user_agent_rotation=True,
                logger=logger
            )
            success = comment_spider.crawl_comments(
                poi_id=str(poi_id),
                poi_name=poi_name,
                max_pages=2  # 爬取2页作为示例 / Scrape 2 pages as example
            )
            
            if success:
                print(f"✓ 评论爬取完成，数据保存在 / Comment scraping completed, data saved in: ./Datasets/")
            else:
                print("✗ 评论爬取失败 / Comment scraping failed")
        else:
            print("未在列表中找到匹配的景点 / Matching attraction not found in list")
    else:
        print("未获取到景点列表 / No attraction list retrieved")


def main():
    """
    主函数 - 运行所有示例 / Main Function - Run All Examples
    """
    print("="*60)
    print("携程数据爬虫 - 使用示例 / Ctrip Data Spider - Usage Examples")
    print("="*60)
    print("\n本程序演示如何使用各个模块进行数据爬取")
    print("This program demonstrates how to use each module for data scraping")
    print("注意: 请遵守网站使用协议，合理控制爬取频率")
    print("Note: Please comply with website terms of service and control scraping frequency reasonably")
    
    # 创建输出目录 / Create output directories
    os.makedirs('./Datasets', exist_ok=True)
    os.makedirs('./logs', exist_ok=True)
    
    try:
        # 运行各个示例（可以注释掉不需要的示例）/ Run examples (can comment out unwanted examples)
        
        # 示例1: 搜索景点ID / Example 1: Search Attraction ID
        example_1_search_sight_id()
        
        # 示例2: 获取景点列表 / Example 2: Get Attraction List
        attractions = example_2_get_attraction_list()
        
        # 示例3: 获取景点详情 / Example 3: Get Attraction Details
        example_3_get_attraction_detail()
        
        # 示例4: 爬取评论 / Example 4: Scrape Comments
        example_4_crawl_comments()
        
        # 示例5: 完整工作流程（可选）/ Example 5: Complete Workflow (optional)
        # example_5_complete_workflow()
        
        print("\n" + "="*60)
        print("所有示例运行完成！/ All examples completed!")
        print("="*60)
        print("\n输出文件 / Output Files:")
        print("  - 景点列表 / Attraction List: ./attractions_list.json")
        print("  - 评论数据 / Comments Data: ./Datasets/*.csv")
        print("  - 日志文件 / Log Files: ./logs/*.log")
        
    except KeyboardInterrupt:
        print("\n\n用户中断程序 / User interrupted program")
    except Exception as e:
        print(f"\n\n发生错误 / Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

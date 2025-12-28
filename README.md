# Ctrip Data Spider & Analysis / 携程数据爬虫与分析

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### 📖 Overview

This project is a comprehensive web scraping tool for collecting tourism attraction data from Ctrip (携程), one of China's largest online travel platforms. It provides functionality to search attractions, retrieve attraction lists, fetch detailed information, and collect user reviews for data analysis and research purposes.

### 📖 项目简介

本项目是一个用于从携程网（中国最大的在线旅游平台之一）收集旅游景点数据的综合网络爬虫工具。它提供了搜索景点、获取景点列表、获取详细信息以及收集用户评论等功能，用于数据分析和研究。

### ✨ Features

- **Attraction ID Search**: Search for attraction IDs by keywords
- **Attraction List Retrieval**: Get attraction lists by district/region
- **Attraction Details**: Fetch comprehensive information about specific attractions
- **Comment Scraping**: Collect user reviews and ratings in bulk
- **Anti-Spider Protection**: Built-in request optimization and User-Agent rotation
- **Data Export**: Export data in JSON and CSV formats
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

### ✨ 主要功能

- **景点ID搜索**: 通过关键词搜索景点ID
- **景点列表获取**: 按地区获取景点列表
- **景点详情**: 获取特定景点的详细信息
- **评论爬取**: 批量收集用户评论和评分
- **反爬虫保护**: 内置请求优化和User-Agent轮换
- **数据导出**: 以JSON和CSV格式导出数据
- **详细日志**: 用于调试和监控的详细日志记录

### 🚀 Quick Start

### 🚀 快速开始

#### Prerequisites

- Python 3.7 or higher
- Required packages: `requests`, `beautifulsoup4`

#### 环境要求

- Python 3.7 或更高版本
- 所需包: `requests`, `beautifulsoup4`

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/colorwinds/Ctrip_Data_Spider_Analysis.git
cd Ctrip_Data_Spider_Analysis-main
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4
```

#### 安装步骤

1. 克隆仓库:
```bash
git clone https://github.com/colorwinds/Ctrip_Data_Spider_Analysis.git
cd Ctrip_Data_Spider_Analysis-main
```

2. 安装依赖:
```bash
pip install requests beautifulsoup4
```

#### Basic Usage / 基本使用

**Quick Start Example / 快速开始示例:**
```bash
python quick_start.py
```

**Full Example / 完整示例:**
```bash
python main_example.py
```

**Test Imports / 测试导入:**
```bash
python test_imports.py
```

### 📚 Project Structure / 项目结构

```
Ctrip_Data_Spider_Analysis-main/
│
├── Ctrip_Spider/              # Main spider module / 主爬虫模块
│   ├── sight_id.py           # Attraction ID search / 景点ID搜索
│   ├── sight_list.py         # Attraction list retrieval / 景点列表获取
│   ├── sight_detail.py       # Attraction detail fetching / 景点详情获取
│   ├── sight_comments.py     # Comment scraping / 评论爬取
│   ├── anti_spider.py        # Anti-spider protection / 反爬虫保护
│   ├── log.py                # Logging utilities / 日志工具
│   └── config.py             # Configuration / 配置文件
│
├── Datasets/                  # Output directory for scraped data / 爬取数据输出目录
├── logs/                      # Log files / 日志文件
├── utils/                     # Utility functions / 工具函数
│
├── main_example.py            # Complete usage examples / 完整使用示例
├── quick_start.py             # Quick start guide / 快速开始指南
├── test_imports.py            # Import testing / 导入测试
│
├── README.md                  # This file / 本文件
├── main_example.py            # Complete usage examples / 完整使用示例
└── INPUT_EXAMPLES.md          # Input parameter examples / 输入参数示例
```

### 🔧 Usage Examples

### 🔧 使用示例

#### Example 1: Search Attraction ID / 示例1: 搜索景点ID

```python
from Ctrip_Spider.sight_id import SightId
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
searcher = SightId(
    delay_range=(1, 2),
    use_user_agent_rotation=True,
    logger=logger
)

# Search for attraction ID by keyword / 通过关键词搜索景点ID
sight_id = searcher.search_sight_id("Yellow Crane Tower")  # or "黄鹤楼"
print(f"Attraction ID: {sight_id}")  # 景点ID
```

#### Example 2: Get Attraction List / 示例2: 获取景点列表

```python
from Ctrip_Spider.sight_list import CtripAttractionScraper
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
scraper = CtripAttractionScraper(
    timeout=10,
    delay_range=(1, 2),
    use_user_agent_rotation=True,
    logger=logger
)

# Get attractions from Beijing (district_id=9) / 获取北京地区的景点（district_id=9）
attractions = scraper.get_attractions_with_pagination(
    district_id=9,      # Beijing / 北京
    pages=2,            # Number of pages / 页数
    count_per_page=5    # Count per page / 每页数量
)
```

#### Example 3: Fetch Attraction Details / 示例3: 获取景点详情

```python
from Ctrip_Spider.sight_detail import AttractionDetailFetcher
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
fetcher = AttractionDetailFetcher(
    delay_range=(1, 2),
    use_user_agent_rotation=True,
    logger=logger
)

# Fetch attraction details by POI ID / 通过POI ID获取景点详情
detail = fetcher.get_detail(poi_id=87211)
if detail.get('success'):
    print(f"Name: {detail.get('poi_name')}")           # 景点名称
    print(f"Price: {detail.get('ticket_price')}")     # 门票价格
```

#### Example 4: Scrape Comments / 示例4: 爬取评论

```python
from Ctrip_Spider.sight_comments import CtripCommentSpider
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
spider = CtripCommentSpider(
    output_dir='./Datasets',    # Output directory / 输出目录
    delay_range=(1, 2),
    use_user_agent_rotation=True,
    logger=logger
)

# Scrape comments for an attraction / 爬取景点评论
success = spider.crawl_comments(
    poi_id='76865',                    # POI ID (string) / POI ID（字符串）
    poi_name='Xinghai Square',         # Attraction name / 景点名称 (e.g., '星海广场')
    max_pages=10                       # Maximum pages to scrape / 最大爬取页数
)
```

### 📊 Output Data Format / 输出数据格式

#### Attraction List (JSON) / 景点列表 (JSON)
- **File / 文件**: `attractions_list.json`
- **Fields / 字段**: name（名称）, id（ID）, poi_id（POI ID）, rating（评分）, review_count（评论数）, price（价格）, address（地址）等

#### Comments (CSV) / 评论数据 (CSV)
- **File / 文件**: `{poi_id}_{attraction_name}.csv` / `{poi_id}_{景点名称}.csv`
- **Fields / 字段**: Comment ID（评论ID）, User Name（用户昵称）, Rating（总体评分）, Comment Content（评论内容）, Post Time（发布时间）, Useful Count（有用数）, Reply Count（回复数）, Travel Type（出行类型）, User Location（用户所在地）, Play Duration（游玩时长）, Image Count（图片数量）, Image URLs（图片链接列表）, Scenic Rating（景色评分）, Fun Rating（趣味评分）, Value Rating（性价比评分）, Recommended Items（推荐项目）

### ⚙️ Configuration

### ⚙️ 配置说明

#### Delay Settings / 延迟设置
```python
delay_range=(1, 3)  # Request delay range in seconds / 请求延迟范围（秒）
```

#### User-Agent Rotation / User-Agent轮换
```python
use_user_agent_rotation=True  # Recommended / 推荐启用
```

#### Proxy Support (Optional) / 代理支持（可选）
```python
proxies = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
]
use_proxy=True  # Enable proxy / 启用代理
```

### 🗺️ Common District IDs

### 🗺️ 常见地区ID参考

| District | ID |
|----------|-----|
| Beijing  | 9   |
| Shanghai | 2   |
| Guangzhou| 7   |
| Shenzhen | 26  |
| Hangzhou | 14  |
| Chengdu  | 104 |
| Xi'an    | 7   |
| Nanjing  | 6   |

| 地区 | ID |
|------|-----|
| 北京 | 9   |
| 上海 | 2   |
| 广州 | 7   |
| 深圳 | 26  |
| 杭州 | 14  |
| 成都 | 104 |
| 西安 | 7   |
| 南京 | 6   |

### ⚠️ Important Notes

1. **Compliance**: Please comply with the website's robots.txt and terms of service
2. **Rate Limiting**: Set reasonable delay ranges (1-3 seconds) to avoid overloading servers
3. **Data Usage**: Scraped data is for learning and research purposes only
4. **Error Handling**: Monitor log files for debugging
5. **Proxy Usage**: Ensure proxy availability if using proxies

### ⚠️ 重要提示

1. **遵守协议**: 请遵守网站的robots.txt和使用协议
2. **合理频率**: 设置合理的延迟范围（1-3秒）以避免服务器过载
3. **数据使用**: 爬取的数据仅供学习和研究使用
4. **错误处理**: 监控日志文件以进行调试
5. **代理使用**: 如果使用代理，请确保代理可用

### 🐛 Troubleshooting

**Q: Cannot retrieve data?**
- Check network connection
- Review log files for error details
- Try increasing delay time
- Check if access is restricted

**Q: Comment scraping failed?**
- Verify POI ID is correct
- Check if the attraction has comments
- Review log files for specific errors

**Q: How to get more district IDs?**
- Use browser developer tools to inspect network requests on Ctrip website
- Or try different district_id values using `sight_list.py`

### 🐛 常见问题

**Q: 无法获取数据？**
- 检查网络连接
- 查看日志文件了解错误详情
- 尝试增加延迟时间
- 检查是否被限制访问

**Q: 评论爬取失败？**
- 确认POI ID是否正确
- 检查景点是否有评论
- 查看日志文件了解具体错误

**Q: 如何获取更多地区ID？**
- 使用浏览器开发者工具查看携程网站的网络请求
- 或使用 `sight_list.py` 尝试不同的district_id值

### 📖 Documentation

- [Complete Usage Examples](main_example.py) - Run `python main_example.py` for detailed examples
- [Input Parameter Examples](INPUT_EXAMPLES.md)
- [Anti-Spider Strategy](Ctrip_Spider/ANTI_SPIDER_README.md)

### 📖 相关文档

- [完整使用示例](main_example.py) - 运行 `python main_example.py` 查看详细示例
- [输入参数示例](INPUT_EXAMPLES.md)
- [反爬虫策略说明](Ctrip_Spider/ANTI_SPIDER_README.md)

### 📝 License

This project is for educational and research purposes only. Please respect the website's terms of service and use responsibly.

### 📝 许可证

本项目仅供教育和研究使用。请尊重网站的服务条款并负责任地使用。

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

---

<a name="中文"></a>
## 中文

*Note: The Chinese section above contains all Chinese translations. This section is kept for navigation purposes.*

*注：上方的中文部分已包含所有中文翻译。此部分保留用于导航目的。*

---

## 📧 Contact / 联系方式

If you have any questions or suggestions, please feel free to open an issue.

如有任何问题或建议，请随时提交 issue。

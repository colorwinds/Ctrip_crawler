# 输入参数示例大全

本文档提供项目中所有模块的输入参数示例。

## 📋 目录

1. [搜索景点ID](#1-搜索景点id)
2. [获取景点列表](#2-获取景点列表)
3. [获取景点详情](#3-获取景点详情)
4. [爬取评论](#4-爬取评论)
5. [批量操作](#5-批量操作)

---

## 1. 搜索景点ID

### 输入参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `keyword` | str | 是 | 景点关键词 | "黄鹤楼" |

### 代码示例

```python
from Ctrip_Spider.sight_id import SightId
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
searcher = SightId(use_user_agent_rotation=True, logger=logger)

# 输入示例
sight_id = searcher.search_sight_id("黄鹤楼")
print(sight_id)  # 输出: 景点ID
```

### 输入示例列表

```python
# 示例1: 著名景点
keywords = [
    "黄鹤楼",
    "故宫",
    "天安门",
    "长城",
    "西湖",
    "外滩",
    "东方明珠",
]

# 示例2: 城市地标
keywords = [
    "北京天坛",
    "上海城隍庙",
    "广州塔",
    "深圳世界之窗",
]

# 示例3: 自然景观
keywords = [
    "黄山",
    "泰山",
    "华山",
    "九寨沟",
    "张家界",
]
```

---

## 2. 获取景点列表

### 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `district_id` | int | 是 | - | 地区ID |
| `page` | int | 否 | 1 | 页码 |
| `count` | int | 否 | 20 | 每页数量 |

### 地区ID参考表

| 地区 | ID | 说明 |
|------|-----|------|
| 北京 | 9 | 首都 |
| 上海 | 2 | 直辖市 |
| 广州 | 7 | 省会城市 |
| 深圳 | 26 | 经济特区 |
| 杭州 | 14 | 省会城市 |
| 成都 | 104 | 省会城市 |
| 西安 | 7 | 省会城市 |
| 南京 | 6 | 省会城市 |

### 代码示例

```python
from Ctrip_Spider.sight_list import CtripAttractionScraper
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
scraper = CtripAttractionScraper(use_user_agent_rotation=True, logger=logger)

# 输入示例1: 获取单页数据
attractions = scraper.get_attractions_list(
    district_id=9,    # 北京
    page=1,
    count=20
)

# 输入示例2: 获取多页数据
all_attractions = scraper.get_attractions_with_pagination(
    district_id=9,        # 北京
    pages=5,              # 获取5页
    count_per_page=20     # 每页20个
)
```

### 输入示例列表

```python
# 示例1: 获取北京景点（第1页，20个）
district_id = 9
page = 1
count = 20

# 示例2: 获取上海景点（第1页，10个）
district_id = 2
page = 1
count = 10

# 示例3: 获取广州景点（前3页，每页15个）
district_id = 7
pages = 3
count_per_page = 15
```

---

## 3. 获取景点详情

### 输入参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `poi_id` | int | 是 | 景点POI ID | 87211 |

### 如何获取POI ID？

1. **从景点列表中获取**: 使用 `sight_list.py` 获取景点列表，每个景点有 `poi_id` 字段
2. **从网站获取**: 访问携程网站，查看URL中的POI ID

### 代码示例

```python
from Ctrip_Spider.sight_detail import AttractionDetailFetcher
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
fetcher = AttractionDetailFetcher(use_user_agent_rotation=True, logger=logger)

# 输入示例
detail = fetcher.get_detail(87211)

if detail['success']:
    print(f"景点名称: {detail['poi_name']}")
    print(f"门票价格: {detail['ticket_price']}")
```

### 输入示例列表

```python
# 示例POI ID列表（需要根据实际情况获取）
poi_ids = [
    87211,   # 示例POI ID 1
    76865,   # 星海广场
    75628,   # 棒棰岛
    75633,   # 大连森林动物园
]

# 批量获取详情
for poi_id in poi_ids:
    detail = fetcher.get_detail(poi_id)
    if detail['success']:
        print(f"{detail['poi_name']}: {detail['ticket_price']}")
```

---

## 4. 爬取评论

### 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `poi_id` | str | 是 | - | 景点POI ID（字符串格式） |
| `poi_name` | str | 是 | - | 景点名称 |
| `max_pages` | int | 否 | 100 | 最大爬取页数 |

### 代码示例

```python
from Ctrip_Spider.sight_comments import CtripCommentSpider
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
spider = CtripCommentSpider(
    output_dir='./Datasets',
    use_user_agent_rotation=True,
    logger=logger
)

# 输入示例
success = spider.crawl_comments(
    poi_id='76865',        # POI ID（字符串）
    poi_name='星海广场',    # 景点名称
    max_pages=10           # 爬取10页
)
```

### 输入示例列表

```python
# 示例1: 单个景点
poi_id = '76865'
poi_name = '星海广场'
max_pages = 10

# 示例2: 多个景点（逐个爬取）
pois = [
    ('76865', '星海广场', 10),
    ('75628', '棒棰岛', 5),
    ('75633', '大连森林动物园', 8),
]

for poi_id, poi_name, max_pages in pois:
    spider.crawl_comments(poi_id, poi_name, max_pages)
```

---

## 5. 批量操作

### 批量爬取评论

```python
from Ctrip_Spider.sight_comments import CtripCommentSpider
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")
spider = CtripCommentSpider(
    output_dir='./Datasets',
    use_user_agent_rotation=True,
    logger=logger
)

# 输入: 景点列表
poi_list = [
    ['76865', '星海广场'],
    ['75628', '棒棰岛'],
    ['75633', '大连森林动物园'],
    ['75634', '大连老虎滩海洋公园'],
]

# 批量爬取
results = spider.crawl_multiple_pois(
    poi_list=poi_list,
    max_pages=10  # 每个景点爬取10页
)

# 查看结果
for poi, success in results.items():
    print(f"{poi}: {'成功' if success else '失败'}")
```

### 完整工作流程示例

```python
from Ctrip_Spider.sight_id import SightId
from Ctrip_Spider.sight_list import CtripAttractionScraper
from Ctrip_Spider.sight_comments import CtripCommentSpider
from Ctrip_Spider.log import CtripSpiderLogger

logger = CtripSpiderLogger("Workflow", "logs")

# 步骤1: 搜索景点ID
searcher = SightId(use_user_agent_rotation=True, logger=logger)
sight_id = searcher.search_sight_id("黄鹤楼")

# 步骤2: 获取景点列表，找到对应的POI ID
scraper = CtripAttractionScraper(use_user_agent_rotation=True, logger=logger)
attractions = scraper.get_attractions_list(district_id=9, page=1, count=50)

# 找到目标景点
target = None
for attr in attractions:
    if attr['id'] == sight_id:
        target = attr
        break

if target:
    # 步骤3: 爬取评论
    spider = CtripCommentSpider(
        output_dir='./Datasets',
        use_user_agent_rotation=True,
        logger=logger
    )
    spider.crawl_comments(
        poi_id=str(target['poi_id']),
        poi_name=target['name'],
        max_pages=10
    )
```

---

## 📝 输入参数总结表

### SightId (搜索景点ID)

```python
# 初始化
searcher = SightId(
    delay_range=(1, 3),              # 延迟范围（可选）
    proxies=None,                    # 代理列表（可选）
    use_proxy=False,                 # 是否使用代理（可选）
    use_user_agent_rotation=True,    # User-Agent轮换（推荐）
    logger=None                      # 日志记录器（可选）
)

# 方法调用
sight_id = searcher.search_sight_id("关键词")
```

### CtripAttractionScraper (获取景点列表)

```python
# 初始化
scraper = CtripAttractionScraper(
    timeout=10,                      # 超时时间（可选）
    delay_range=(1, 3),              # 延迟范围（可选）
    proxies=None,                    # 代理列表（可选）
    use_proxy=False,                 # 是否使用代理（可选）
    use_user_agent_rotation=True,    # User-Agent轮换（推荐）
    logger=None                      # 日志记录器（可选）
)

# 方法调用
attractions = scraper.get_attractions_list(
    district_id=9,    # 地区ID（必填）
    page=1,           # 页码（可选，默认1）
    count=20          # 每页数量（可选，默认20）
)
```

### AttractionDetailFetcher (获取景点详情)

```python
# 初始化
fetcher = AttractionDetailFetcher(
    delay_range=(1, 3),              # 延迟范围（可选）
    proxies=None,                    # 代理列表（可选）
    use_proxy=False,                 # 是否使用代理（可选）
    use_user_agent_rotation=True,    # User-Agent轮换（推荐）
    logger=None                      # 日志记录器（可选）
)

# 方法调用
detail = fetcher.get_detail(87211)  # POI ID（必填）
```

### CtripCommentSpider (爬取评论)

```python
# 初始化
spider = CtripCommentSpider(
    output_dir='./Datasets',         # 输出目录（可选）
    delay_range=(1, 3),              # 延迟范围（可选）
    proxies=None,                    # 代理列表（可选）
    use_proxy=False,                # 是否使用代理（可选）
    use_user_agent_rotation=True,   # User-Agent轮换（推荐）
    logger=None                     # 日志记录器（可选）
)

# 方法调用
success = spider.crawl_comments(
    poi_id='76865',        # POI ID（必填，字符串）
    poi_name='星海广场',    # 景点名称（必填）
    max_pages=100          # 最大页数（可选，默认100）
)
```

---

## ⚠️ 注意事项

1. **POI ID vs Sight ID**: 
   - `sight_id` 是景点ID，用于搜索
   - `poi_id` 是POI ID，用于获取详情和评论
   - 两者不同，需要区分使用

2. **地区ID获取**: 
   - 可以通过浏览器开发者工具查看携程网站的网络请求
   - 或者尝试不同的ID值

3. **延迟设置**: 
   - 建议设置 `delay_range=(1, 3)` 避免请求过快
   - 大规模爬取建议增加延迟

4. **数据保存**: 
   - 评论数据自动保存为CSV格式
   - 文件路径: `./Datasets/{poi_id}_{景点名称}.csv`

---

## 🔗 相关文档

- [完整使用示例](main_example.py) - 运行 `python main_example.py` 查看详细示例
- [反爬虫策略说明](Ctrip_Spider/ANTI_SPIDER_README.md)
- [项目主README](README.md)


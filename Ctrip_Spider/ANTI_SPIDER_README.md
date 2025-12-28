# 反爬虫策略使用指南

本项目已集成增强的反爬虫策略，包括User-Agent轮换、代理池管理等功能。

## 📋 功能特性

### 1. User-Agent轮换
- ✅ 内置20+个常见User-Agent
- ✅ 支持随机和轮询两种模式
- ✅ 自动统计使用情况
- ✅ 可自定义User-Agent列表

### 2. 代理池管理
- ✅ 代理健康检查
- ✅ 自动标记失败代理
- ✅ 支持HTTP/HTTPS/SOCKS5代理
- ✅ 代理使用统计

### 3. 请求优化
- ✅ 随机延迟
- ✅ 请求统计
- ✅ 错误处理

## 🚀 快速开始

### 基本使用（仅User-Agent轮换）

```python
from sight_id import SightId
from log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")

# 创建爬虫实例，启用User-Agent轮换
sight_id_searcher = SightId(
    delay_range=(1, 3),
    use_user_agent_rotation=True,  # 启用User-Agent轮换
    logger=logger
)

# 使用爬虫
sight_id = sight_id_searcher.search_sight_id("黄鹤楼")
```

### 使用代理

```python
from sight_comments import CtripCommentSpider
from log import CtripSpiderLogger

logger = CtripSpiderLogger("MySpider", "logs")

# 配置代理列表
proxies = [
    'http://proxy1.example.com:8080',
    'http://user:pass@proxy2.example.com:8080',
    'socks5://proxy3.example.com:1080',
]

# 创建爬虫实例，启用代理和User-Agent轮换
comment_spider = CtripCommentSpider(
    output_dir='./Datasets',
    delay_range=(1, 3),
    proxies=proxies,
    use_proxy=True,  # 启用代理
    use_user_agent_rotation=True,  # 启用User-Agent轮换
    logger=logger
)

# 使用爬虫
comment_spider.crawl_comments('76865', '星海广场', max_pages=10)
```

## 📖 详细说明

### User-Agent轮换模式

#### 随机模式（推荐）
```python
optimizer = EnhancedRequestOptimizer(
    rotation_mode='random',  # 随机选择User-Agent
    use_user_agent_rotation=True
)
```

#### 轮询模式
```python
optimizer = EnhancedRequestOptimizer(
    rotation_mode='round_robin',  # 按顺序轮换User-Agent
    use_user_agent_rotation=True
)
```

### 代理池管理

#### 添加代理
```python
from anti_spider import ProxyPool

proxy_pool = ProxyPool(proxies=[
    'http://proxy1:8080',
    'http://proxy2:8080',
])

# 添加新代理
proxy_pool.add_proxy('http://proxy3:8080')
```

#### 检查代理可用性
```python
# 检查单个代理
is_valid = proxy_pool.check_proxy('http://proxy1:8080')

# 检查所有代理
proxy_pool.check_all_proxies()
```

#### 获取代理统计
```python
stats = proxy_pool.get_stats()
print(f"总数: {stats['total']}")
print(f"可用: {stats['active']}")
print(f"失败: {stats['failed']}")
```

### 延迟配置

```python
# 设置延迟范围为1-3秒
optimizer = EnhancedRequestOptimizer(
    delay_range=(1, 3)
)

# 手动设置延迟
optimizer.set_delay()
```

## 🔧 配置参数

所有配置参数都在 `config.py` 文件中：

```python
# 延迟配置
DELAY_RANGE = (1, 3)  # 请求延迟范围（秒）

# User-Agent配置
USE_USER_AGENT_ROTATION = True  # 是否启用User-Agent轮换
USER_AGENT_ROTATION_MODE = 'random'  # 轮换模式

# 代理配置
USE_PROXY = False  # 是否启用代理
PROXIES = []  # 代理列表
PROXY_MAX_FAILS = 3  # 代理失败阈值
```

## 📝 已更新的模块

以下模块已集成反爬虫策略：

1. ✅ `sight_id.py` - 景点ID搜索器
2. ✅ `sight_list.py` - 景点列表爬取器
3. ✅ `sight_detail.py` - 景点详情获取器
4. ✅ `sight_comments.py` - 评论爬虫

## 🎯 使用建议

### 1. 延迟设置
- **小规模爬取**: `delay_range=(1, 2)` - 1-2秒延迟
- **中等规模**: `delay_range=(2, 4)` - 2-4秒延迟
- **大规模爬取**: `delay_range=(3, 6)` - 3-6秒延迟

### 2. User-Agent轮换
- 建议始终启用 `use_user_agent_rotation=True`
- 随机模式更适合大规模爬取
- 轮询模式适合需要均匀分布的场景

### 3. 代理使用
- 如果没有代理，设置 `use_proxy=False`
- 代理格式: `http://host:port` 或 `http://user:pass@host:port`
- 定期检查代理可用性: `optimizer.check_proxies()`

### 4. 错误处理
- 代理失败会自动标记，避免重复使用
- 超过失败阈值的代理会被标记为不活跃
- 建议定期检查代理池状态

## 🔍 查看统计信息

```python
# 获取优化器统计
stats = optimizer.get_stats()
print(stats)

# 输出示例:
# {
#     'request_count': 100,
#     'user_agent_stats': {
#         'total': 20,
#         'usage_count': {...}
#     },
#     'proxy_stats': {
#         'total': 5,
#         'active': 4,
#         'failed': 1,
#         'stats': {...}
#     }
# }
```

## ⚠️ 注意事项

1. **遵守robots.txt**: 请遵守目标网站的robots.txt协议
2. **合理使用**: 不要过于频繁地请求，避免对服务器造成压力
3. **代理质量**: 使用高质量的代理可以提高成功率
4. **延迟设置**: 根据实际情况调整延迟范围
5. **日志监控**: 定期查看日志，及时发现和解决问题

## 📚 更多示例

查看 `example_anti_spider.py` 文件获取更多使用示例。

## 🐛 问题排查

### User-Agent不生效
- 检查 `use_user_agent_rotation` 是否设置为 `True`
- 查看日志确认User-Agent是否正确设置

### 代理无法使用
- 检查代理格式是否正确
- 使用 `check_proxy()` 测试代理可用性
- 查看代理统计信息，确认代理状态

### 请求被限制
- 增加延迟范围
- 启用代理
- 检查User-Agent是否正常轮换

## 📞 支持

如有问题，请查看日志文件或提交Issue。


# 团购商品评价 API 文档

## 概述

团购商品评价系统提供完整的商品评价、回复、点赞功能，支持用户对购买的商品进行评分和评论。

## 数据库表结构

### 1. good_price_evaluates (评价表)
```
evaluateid VARCHAR(50) PRIMARY KEY    # 评价ID (UUID)
goodpriceid VARCHAR(50)               # 商品ID
uid INTEGER                           # 评价用户ID
orderid VARCHAR(50)                   # 关联订单ID
content TEXT                          # 评价内容
images TEXT                           # 图片列表 (JSON数组)
rating INTEGER                        # 评分 (1-5星)
likenum INTEGER DEFAULT 0             # 点赞数
replynum INTEGER DEFAULT 0            # 回复数
createtime DATETIME                   # 创建时间
```

### 2. good_price_evaluate_replies (评价回复表)
```
replyid VARCHAR(50) PRIMARY KEY       # 回复ID (UUID)
evaluateid VARCHAR(50)                # 评价ID
goodpriceid VARCHAR(50)               # 商品ID
uid INTEGER                           # 回复用户ID
touid INTEGER                         # 被回复用户ID
content TEXT                          # 回复内容
createtime DATETIME                   # 创建时间
```

### 3. good_price_evaluate_likes (评价点赞表)
```
evaluateid VARCHAR(50)                # 评价ID
uid INTEGER                           # 点赞用户ID
likeuid INTEGER                       # 被点赞评价的用户ID
goodpriceid VARCHAR(50)               # 商品ID
createtime DATETIME                   # 创建时间
type INTEGER DEFAULT 1                # 类型 (1: 点赞)
```

## API 接口

### 获取商品评价列表

**端点**: `POST /grouppurchase/getEvaluateGoodPriceList`

**请求参数**:
```json
{
  "goodpriceid": "商品ID (必填)",
  "currentIndex": 0  // 可选，默认0，每页20条
}
```

**响应格式**:
```json
{
  "success": true,
  "data": {
    "evaluates": [
      {
        "evaluateid": "评价ID",
        "goodpriceid": "商品ID",
        "uid": 1000,
        "orderid": "订单ID",
        "content": "评价内容",
        "images": "[\"图片URL1\",\"图片URL2\"]",
        "rating": 5,
        "likenum": 10,
        "replynum": 2,
        "createtime": "2025-01-15T10:30:00"
      }
    ],
    "total": 100
  }
}
```

**使用示例** (curl):
```bash
curl -X POST http://localhost:5000/grouppurchase/getEvaluateGoodPriceList \
  -H "Content-Type: application/json" \
  -d '{
    "goodpriceid": "5cee1569-4dad-41e0-8e1d-7bd877aa0e9f",
    "currentIndex": 0
  }'
```

## 服务层方法

### 1. 添加评价
```python
from api.services.group_purchase_service import GroupPurchaseService

evaluateid = GroupPurchaseService.add_evaluate({
    'goodpriceid': '商品ID',
    'uid': 1000,
    'orderid': '订单ID',
    'content': '评价内容',
    'rating': 5,
    'images': '["图片URL1","图片URL2"]'
})
```

### 2. 获取评价列表
```python
evaluates = GroupPurchaseService.get_evaluate_list(
    goodpriceid='商品ID',
    current_index=0
)
```

### 3. 添加评价回复
```python
replyid = GroupPurchaseService.add_evaluate_reply({
    'evaluateid': '评价ID',
    'goodpriceid': '商品ID',
    'uid': 1001,
    'touid': 1000,
    'content': '回复内容'
})
```

### 4. 获取评价回复列表
```python
replies = GroupPurchaseService.get_evaluate_replies(evaluateid='评价ID')
```

### 5. 点赞评价
```python
success = GroupPurchaseService.add_evaluate_like(
    evaluateid='评价ID',
    uid=1002,
    likeuid=1000,
    goodpriceid='商品ID'
)
```

### 6. 取消点赞
```python
success = GroupPurchaseService.remove_evaluate_like(
    evaluateid='评价ID',
    uid=1002
)
```

## 数据模型

### EvaluateActivity (评价活动对象)
```python
{
    "evaluateid": str,     # 评价ID
    "goodpriceid": str,    # 商品ID
    "uid": int,            # 用户ID
    "orderid": str,        # 订单ID
    "content": str,        # 评价内容
    "images": str,         # 图片列表 (JSON字符串)
    "rating": int,         # 评分 (1-5)
    "likenum": int,        # 点赞数
    "replynum": int,       # 回复数
    "createtime": str      # ISO格式时间
}
```

## 特性说明

### 评分系统
- **评分范围**: 1-5星
- **显示格式**: ⭐⭐⭐⭐⭐
- **平均评分**: 自动计算每个商品的平均评分

### 图片上传
- **格式**: JSON数组字符串
- **示例**: `["https://example.com/pic1.jpg","https://example.com/pic2.jpg"]`
- **建议**: 每个评价最多3-5张图片

### 点赞功能
- 自动更新评价的 `likenum` 字段
- 防重复点赞 (同一用户对同一评价只能点赞一次)
- 支持取消点赞

### 回复功能
- 支持商家回复用户评价
- 支持用户间相互回复
- 自动更新评价的 `replynum` 字段
- 记录回复目标用户 (`touid`)

## 测试数据

系统已包含测试数据:
- **6个商品评价**
  - 超值团购-新鲜水果拼盘: 3条评价 (平均5.0★)
  - 人气爆款-奶茶套餐: 2条评价 (平均4.5★)
  - 居家必备-清洁套装: 1条评价 (平均4.0★)

- **平均评分**: 4.67星
- **5星评价**: 66.7%
- **4星评价**: 33.3%

## 使用建议

### 前端集成
1. 在商品详情页显示评价列表
2. 实现下拉刷新和上拉加载更多
3. 显示评价图片轮播
4. 支持点击查看大图
5. 显示商家回复（如有）

### 性能优化
1. 评价列表分页加载（每页20条）
2. 图片懒加载
3. 对 `goodpriceid` 字段建立索引

### 数据验证
1. 评分必须在1-5之间
2. 评价内容不能为空
3. 只有购买过的用户才能评价（检查orderid）
4. 图片URL格式验证

## 相关文档
- [团购模块主文档](README.md)
- [分类字段变更](GROUP_PURCHASE_CATEGORY_CHANGE.md)
- [图片字段重命名](GROUP_PURCHASE_ALBUMPICS_RENAME.md)

---

**版本**: 1.0.0  
**最后更新**: 2025-01-15  
**维护者**: Development Team

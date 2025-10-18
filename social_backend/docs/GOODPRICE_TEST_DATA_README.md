# GoodPrice 评论测试数据初始化指南

## 📋 概述

这些脚本用于初始化 GoodPrice 商品和评论系统的测试数据。评论系统已更新，`commentid` 现在使用 **Integer 类型**（自动增长）而不是 String UUID。

## 🚀 快速开始

### 方法1: 一键运行（推荐）

```bash
python3 setup_goodprice_test_data.py
```

这会自动执行所有步骤:
1. 创建商品数据
2. 创建评论数据

### 方法2: 分步运行

```bash
# 步骤1: 创建商品数据
python3 init_goodprice_data.py

# 步骤2: 创建评论数据
python3 init_goodprice_comments.py
```

## 📦 脚本说明

### 1. `migrate_commentid.py`
**用途**: 迁移数据库结构，将 `commentid` 从 String 改为 Integer

**何时使用**: 
- 首次部署新的评论系统
- 数据库结构需要更新时

**运行**:
```bash
python3 migrate_commentid.py
```

⚠️ **警告**: 会删除所有现有评论数据!

---

### 2. `init_goodprice_data.py`
**用途**: 创建 GoodPrice 商品测试数据

**创建数据**:
- 12个商品（涵盖多个品类）
- 包含完整的商品信息（标题、价格、品牌等）
- 不同的城市和地区

**运行**:
```bash
python3 init_goodprice_data.py
```

**商品类别包括**:
- 电子产品（iPhone, MacBook, Switch等）
- 家电（戴森吸尘器）
- 美妆（海蓝之谜、雅诗兰黛）
- 玩具（乐高）
- 运动鞋（Nike AJ1）
- 服饰（优衣库）
- 等等...

---

### 3. `init_goodprice_comments.py`
**用途**: 为商品创建评论、回复、点赞测试数据

**创建数据**:
- 每个商品 2-6 条评论
- 40% 的评论会有 1-3 条回复
- 60% 的评论会有 1-5 个点赞
- 评论使用 **Integer commentid**（自动增长）

**特点**:
- ✅ commentid 是 Integer 类型
- ✅ 自动更新商品的 commentnum
- ✅ 真实的评论内容和回复
- ✅ 随机的时间戳和点赞数

**运行**:
```bash
python3 init_goodprice_comments.py
```

---

### 4. `setup_goodprice_test_data.py`
**用途**: 一键运行所有初始化脚本

**功能**:
- 自动依次执行商品和评论数据初始化
- 提供友好的进度提示
- 完成后显示测试建议

**运行**:
```bash
python3 setup_goodprice_test_data.py
```

---

### 5. `test_commentid_integer.py`
**用途**: 测试 Integer commentid 的功能

**测试内容**:
- 创建评论（验证返回 Integer commentid）
- 创建回复
- 获取评论列表
- 评论点赞

**运行**:
```bash
python3 test_commentid_integer.py
```

## 📊 数据统计

运行完成后，你将拥有:

| 数据类型 | 数量 | 说明 |
|---------|------|------|
| GoodPrice | 12+ | 商品数据 |
| GoodPriceComment | 20-60 | 评论（Integer ID） |
| GoodPriceCommentReply | 8-30 | 回复 |
| GoodPriceCommentLike | 12-50 | 点赞 |

## 🧪 API 测试

### 1. 获取评论列表
```bash
curl 'http://127.0.0.1:5000/grouppurchase/getcomment?goodpriceid=[商品ID]&uid=1001'
```

### 2. 发布评论
```bash
curl -X POST 'http://127.0.0.1:5000/grouppurchase/updatecomment' \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "test-token",
    "goodpriceid": "[商品ID]",
    "uid": 1001,
    "content": "这是一条测试评论"
  }'
```

### 3. 评论点赞
```bash
curl -X POST 'http://127.0.0.1:5000/grouppurchase/updateCommentLike' \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "test-token",
    "commentid": 1,
    "uid": 1002,
    "likeuid": 1001,
    "goodpriceid": "[商品ID]"
  }'
```

### 4. 获取商品评价列表
```bash
curl -X POST 'http://127.0.0.1:5000/grouppurchase/getEvaluateGoodPriceList' \
  -H 'Content-Type: application/json' \
  -d '{
    "goodpriceid": "[商品ID]",
    "currentIndex": 0
  }'
```

## ✅ 验证 Integer commentid

创建评论后，检查返回的 `commentid`:

```json
{
  "success": true,
  "commentid": 1    ← Integer 类型，不是 UUID 字符串
}
```

获取评论列表时:
```json
{
  "success": true,
  "data": [
    {
      "commentid": 1,    ← Integer 类型
      "uid": 1001,
      "content": "这个价格真的很划算!",
      ...
    }
  ]
}
```

## 🔧 故障排除

### 问题: 找不到商品数据
**解决**: 先运行 `python3 init_goodprice_data.py` 创建商品

### 问题: commentid 仍是 String 类型
**解决**: 
1. 运行 `python3 migrate_commentid.py` 迁移数据库
2. 重启 Flask 服务器

### 问题: 415 Unsupported Media Type
**解决**: 确保请求头包含 `Content-Type: application/json`

### 问题: CORS 错误
**解决**: 已在 `api/__init__.py` 中配置 CORS，重启服务器

## 📝 注意事项

1. **数据库迁移**: `migrate_commentid.py` 会删除所有现有评论数据
2. **测试环境**: 建议先在测试环境运行
3. **用户ID**: 测试数据使用 1001-1010 的用户ID
4. **Token**: API 调用需要有效的 token（测试时可能需要禁用 @token_required）

## 🎯 推荐流程

首次设置:
```bash
# 1. 迁移数据库（如果需要）
python3 migrate_commentid.py

# 2. 一键初始化所有数据
python3 setup_goodprice_test_data.py

# 3. 测试功能
python3 test_commentid_integer.py
```

后续添加更多数据:
```bash
# 只添加商品
python3 init_goodprice_data.py

# 只添加评论
python3 init_goodprice_comments.py
```

## 📚 相关文件

- `api/models/group_purchase.py` - 数据模型定义
- `api/services/group_purchase_service.py` - 业务逻辑
- `api/controllers/group_purchase.py` - API 端点
- `api/__init__.py` - CORS 配置

## 💡 提示

运行脚本后会显示详细的数据示例和 API 测试命令，请注意查看输出信息！

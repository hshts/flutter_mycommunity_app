# IM模块 - Moment(动态)服务接口文档

## 📋 目录

1. [概述](#概述)
2. [数据模型](#数据模型)
3. [API接口](#api接口)
4. [使用示例](#使用示例)
5. [测试数据](#测试数据)

---

## 概述

### 功能说明

本文档描述了IM模块中关于**动态(Moment)**的所有服务接口实现,包括:

- ✅ 动态发布、删除
- ✅ 动态列表查询(支持分页和话题筛选)
- ✅ 动态详情查询
- ✅ 动态搜索
- ✅ 动态点赞/取消点赞
- ✅ 动态评论/回复
- ✅ 评论删除
- ✅ 评论列表查询
- ✅ 评论点赞/取消点赞

### 技术栈

- **后端框架**: Flask 2.3.2
- **API文档**: Flask-RESTX 1.3.0
- **数据库**: SQLite with Flask-SQLAlchemy 3.0.5
- **ID类型**: Integer (自增主键)

---

## 数据模型

### 1. Moment (动态)

| 字段 | 类型 | 说明 |
|-----|------|------|
| momentid | Integer | 动态ID (主键,自增) |
| uid | Integer | 发布用户ID |
| content | Text | 动态内容 |
| voice | String(500) | 音频文件路径 |
| images | Text | 图片列表 (JSON格式) |
| coverimgwh | String(50) | 封面图宽高比 |
| category | String(100) | 分类/话题 |
| likenum | Integer | 点赞数 (默认0) |
| commentnum | Integer | 评论数 (默认0) |
| createtime | DateTime | 创建时间 |
| updatetime | DateTime | 更新时间 |
| status | Integer | 状态 (1:正常, 0:已删除) |

### 2. MomentComment (动态评论)

| 字段 | 类型 | 说明 |
|-----|------|------|
| commentid | Integer | 评论ID (主键,自增) |
| momentid | Integer | 动态ID (外键) |
| uid | Integer | 评论用户ID |
| touid | Integer | 目标用户ID (评论时为空,回复时有值) |
| content | Text | 评论内容 |
| likenum | Integer | 点赞数 (默认0) |
| replynum | Integer | 回复数 (默认0) |
| createtime | DateTime | 创建时间 |
| status | Integer | 状态 (1:正常, 0:已删除) |

### 3. MomentCommentReply (动态评论回复)

| 字段 | 类型 | 说明 |
|-----|------|------|
| replyid | Integer | 回复ID (主键,自增) |
| commentid | Integer | 评论ID (外键) |
| momentid | Integer | 动态ID |
| uid | Integer | 回复用户ID |
| touid | Integer | 目标用户ID |
| content | Text | 回复内容 |
| createtime | DateTime | 创建时间 |
| status | Integer | 状态 (1:正常, 0:已删除) |

### 4. MomentLike (动态点赞)

| 字段 | 类型 | 说明 |
|-----|------|------|
| likeid | Integer | 点赞ID (主键,自增) |
| momentid | Integer | 动态ID (外键) |
| uid | Integer | 点赞用户ID |
| createtime | DateTime | 创建时间 |

**唯一约束**: (momentid, uid) - 确保同一用户不能重复点赞

### 5. MomentCommentLike (动态评论点赞)

| 字段 | 类型 | 说明 |
|-----|------|------|
| likeid | Integer | 点赞ID (主键,自增) |
| commentid | Integer | 评论ID (外键) |
| uid | Integer | 点赞用户ID |
| createtime | DateTime | 创建时间 |

**唯一约束**: (commentid, uid) - 确保同一用户不能重复点赞评论

---

## API接口

### 1. 发布动态

**接口**: `POST /IM/reportMoment`

**请求参数**:
```json
{
  "uid": 1000,
  "token": "user_token",
  "content": "分享今天的好心情!",
  "voice": "https://example.com/audio.mp3",
  "images": "[\"https://example.com/img1.jpg\", \"https://example.com/img2.jpg\"]",
  "coverimgwh": "16:9",
  "category": "生活分享",
  "captchaVerification": "验证码"
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "发布成功",
  "data": {
    "momentid": 1
  }
}
```

---

### 2. 删除动态

**接口**: `POST /IM/delMoment`

**请求参数**:
```json
{
  "token": "user_token",
  "uid": 1000,
  "momentid": 1
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "删除成功",
  "data": true
}
```

---

### 3. 获取动态列表

**接口**: `POST /IM/getMomentList`

**请求参数**:
```json
{
  "currIndex": 0,
  "subject": "美食"
}
```

**参数说明**:
- `currIndex`: 当前页索引 (从0开始)
- `subject`: 话题筛选 (可选)

**响应**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "list": [
      {
        "momentid": 1,
        "uid": 1000,
        "content": "分享今天的美食 #美食",
        "voice": null,
        "images": "[\"https://example.com/img1.jpg\"]",
        "coverimgwh": "16:9",
        "category": "美食",
        "likenum": 10,
        "commentnum": 5,
        "createtime": "2025-01-15T10:30:00",
        "updatetime": "2025-01-15T10:30:00",
        "status": 1
      }
    ],
    "total": 1
  }
}
```

---

### 4. 获取动态详情

**接口**: `POST /IM/getMomentInfo`

**请求参数**:
```json
{
  "momentid": 1
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "momentid": 1,
    "uid": 1000,
    "content": "分享今天的美食",
    "voice": null,
    "images": "[\"https://example.com/img1.jpg\"]",
    "coverimgwh": "16:9",
    "category": "美食",
    "likenum": 10,
    "commentnum": 5,
    "createtime": "2025-01-15T10:30:00",
    "updatetime": "2025-01-15T10:30:00",
    "status": 1
  }
}
```

---

### 5. 获取用户动态列表

**接口**: `POST /IM/getMomentListByUser`

**请求参数**:
```json
{
  "uid": 1000
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "list": [...],
    "total": 5
  }
}
```

---

### 6. 搜索动态

**接口**: `POST /IM/searchMoment`

**请求参数**:
```json
{
  "content": "美食",
  "currentIndex": 0
}
```

**参数说明**:
- 搜索内容会匹配动态内容和分类字段

**响应**:
```json
{
  "code": 200,
  "msg": "搜索成功",
  "data": {
    "list": [...],
    "total": 3
  }
}
```

---

### 7. 动态点赞

**接口**: `POST /IM/updateMomentLike`

**请求参数**:
```json
{
  "token": "user_token",
  "momentid": 1,
  "uid": 1000
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "点赞成功",
  "data": true
}
```

**已点赞响应**:
```json
{
  "code": 201,
  "msg": "已经点赞过了",
  "data": false
}
```

---

### 8. 取消动态点赞

**接口**: `POST /IM/delMomentLike`

**请求参数**:
```json
{
  "token": "user_token",
  "momentid": 1,
  "uid": 1000
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "取消点赞成功",
  "data": true
}
```

---

### 9. 发布动态评论

**接口**: `POST /IM/updateMomentComment`

**请求参数** (发布评论):
```json
{
  "token": "user_token",
  "momentid": 1,
  "uid": 1000,
  "content": "这个动态很棒!",
  "captchaVerification": "验证码"
}
```

**请求参数** (回复评论):
```json
{
  "commentid": 5,
  "token": "user_token",
  "momentid": 1,
  "uid": 1000,
  "touid": 1001,
  "content": "我也觉得!",
  "captchaVerification": "验证码"
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "评论成功",
  "data": {
    "id": 10
  }
}
```

---

### 10. 删除动态评论

**接口**: `POST /IM/delMomentComment`

**请求参数** (删除评论):
```json
{
  "token": "user_token",
  "commentid": 10,
  "uid": 1000,
  "momentid": 1
}
```

**请求参数** (删除回复):
```json
{
  "token": "user_token",
  "commentid": 10,
  "uid": 1000,
  "replyid": 5,
  "momentid": 1
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "删除成功",
  "data": true
}
```

---

### 11. 获取动态评论列表

**接口**: `GET /IM/getMomentComment?momentid=1`

**请求参数**:
- `momentid`: 动态ID (Query参数)

**响应**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "list": [
      {
        "commentid": 1,
        "momentid": 1,
        "uid": 1000,
        "touid": null,
        "content": "这个动态很棒!",
        "likenum": 3,
        "replynum": 2,
        "createtime": "2025-01-15T11:00:00",
        "status": 1
      }
    ],
    "total": 1
  }
}
```

---

### 12. 动态评论点赞

**接口**: `POST /IM/updateMomentCommentLike`

**请求参数**:
```json
{
  "token": "user_token",
  "commentid": 1,
  "uid": 1000,
  "likeuid": 1001,
  "momentid": 1
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "点赞成功",
  "data": true
}
```

---

### 13. 取消动态评论点赞

**接口**: `POST /IM/delMomentCommentLike`

**请求参数**:
```json
{
  "token": "user_token",
  "commentid": 1,
  "likeuid": 1001,
  "uid": 1000
}
```

**响应**:
```json
{
  "code": 200,
  "msg": "取消点赞成功",
  "data": true
}
```

---

## 使用示例

### Python示例

```python
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 1. 发布动态
def create_moment():
    url = f"{BASE_URL}/IM/reportMoment"
    data = {
        "uid": 1000,
        "token": "user_token",
        "content": "分享一下今天的好心情!",
        "category": "生活分享",
        "images": json.dumps([
            "https://example.com/img1.jpg",
            "https://example.com/img2.jpg"
        ]),
        "coverimgwh": "16:9"
    }
    response = requests.post(url, json=data)
    return response.json()

# 2. 获取动态列表
def get_moment_list():
    url = f"{BASE_URL}/IM/getMomentList"
    data = {
        "currIndex": 0,
        "subject": "生活分享"
    }
    response = requests.post(url, json=data)
    return response.json()

# 3. 动态点赞
def like_moment(momentid):
    url = f"{BASE_URL}/IM/updateMomentLike"
    data = {
        "token": "user_token",
        "momentid": momentid,
        "uid": 1000
    }
    response = requests.post(url, json=data)
    return response.json()

# 4. 发布评论
def add_comment(momentid):
    url = f"{BASE_URL}/IM/updateMomentComment"
    data = {
        "token": "user_token",
        "momentid": momentid,
        "uid": 1000,
        "content": "这个动态很棒!"
    }
    response = requests.post(url, json=data)
    return response.json()
```

### cURL示例

```bash
# 1. 发布动态
curl -X POST http://127.0.0.1:5000/IM/reportMoment \
  -H "Content-Type: application/json" \
  -d '{
    "uid": 1000,
    "token": "user_token",
    "content": "分享今天的好心情!",
    "category": "生活分享"
  }'

# 2. 获取动态列表
curl -X POST http://127.0.0.1:5000/IM/getMomentList \
  -H "Content-Type: application/json" \
  -d '{
    "currIndex": 0,
    "subject": "生活分享"
  }'

# 3. 动态点赞
curl -X POST http://127.0.0.1:5000/IM/updateMomentLike \
  -H "Content-Type: application/json" \
  -d '{
    "token": "user_token",
    "momentid": 1,
    "uid": 1000
  }'

# 4. 获取评论列表
curl -X GET "http://127.0.0.1:5000/IM/getMomentComment?momentid=1"
```

---

## 测试数据

### 数据统计

执行 `python3 add_moment_test_data.py` 后生成的测试数据:

- ✅ **15条动态**: 由用户1000-1004发布
- ✅ **37个点赞**: 分布在前10条动态
- ✅ **28条评论**: 分布在前8条动态
- ✅ **9条回复**: 部分评论有回复
- ✅ **21个评论点赞**: 分布在各评论中

### 测试话题

- 生活分享
- 旅行
- 美食
- 运动健身
- 摄影
- 读书
- 音乐
- 电影

### 测试脚本

```bash
# 1. 初始化数据库表
python3 init_moment_tables.py

# 2. 生成测试数据
python3 add_moment_test_data.py

# 3. 测试API接口
python3 test_moment_api.py
```

---

## 状态码说明

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 201 | 已存在(如已点赞) |
| 400 | 参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 注意事项

1. **ID类型**: 所有ID字段(momentid, commentid, replyid等)均为Integer类型
2. **软删除**: 评论和动态使用软删除(status=0),不实际删除数据
3. **点赞去重**: 使用数据库唯一约束确保同一用户不能重复点赞
4. **计数更新**: 点赞数和评论数实时更新
5. **分页查询**: 默认每页20条记录
6. **话题筛选**: 支持按category字段筛选动态
7. **搜索功能**: 同时搜索content和category字段

---

## API文档地址

启动服务器后访问: `http://127.0.0.1:5000/doc`

可查看完整的Swagger API文档。

---

**文档版本**: 1.0  
**最后更新**: 2025年1月  
**维护者**: Backend Team

# Activity 模块评论相关 API 文档

## 概述

Activity 模块的评论系统提供完整的评论、回复、点赞功能，支持用户对活动进行评论和互动。

## 数据库表结构

### 1. activity_comments (活动评论表)
```sql
commentid VARCHAR(50) PRIMARY KEY    # 评论ID (UUID)
actid VARCHAR(50) NOT NULL           # 活动ID
uid INTEGER NOT NULL                 # 评论用户ID
touid INTEGER                        # 目标用户ID (可选)
content TEXT NOT NULL                # 评论内容
likenum INTEGER DEFAULT 0            # 点赞数
replynum INTEGER DEFAULT 0           # 回复数
createtime DATETIME                  # 创建时间
status INTEGER DEFAULT 1             # 状态 (1: 正常, 0: 已删除)

INDEX: actid                         # 活动ID索引
```

### 2. activity_comment_replies (活动评论回复表)
```sql
replyid VARCHAR(50) PRIMARY KEY      # 回复ID (UUID)
commentid VARCHAR(50) NOT NULL       # 评论ID
actid VARCHAR(50) NOT NULL           # 活动ID
uid INTEGER NOT NULL                 # 回复用户ID
touid INTEGER NOT NULL               # 被回复用户ID
content TEXT NOT NULL                # 回复内容
createtime DATETIME                  # 创建时间
status INTEGER DEFAULT 1             # 状态 (1: 正常, 0: 已删除)

INDEX: commentid                     # 评论ID索引
```

### 3. activity_comment_likes (活动评论点赞表)
```sql
id INTEGER PRIMARY KEY AUTO_INCREMENT  # 自增ID
commentid VARCHAR(50) NOT NULL         # 评论ID
actid VARCHAR(50) NOT NULL             # 活动ID
uid INTEGER NOT NULL                   # 点赞用户ID
likeuid INTEGER NOT NULL               # 被点赞评论的用户ID
createtime DATETIME                    # 创建时间
type INTEGER DEFAULT 1                 # 类型 (1: 点赞)

INDEX: commentid                       # 评论ID索引
UNIQUE: (commentid, uid)               # 联合唯一索引
```

## API 接口

### 1. 获取活动评论列表

**端点**: `GET /Activity/getCommentList`

**请求参数**:
- `actid` (必填): 活动ID
- `uid` (可选): 用户ID，用于判断用户是否点赞过评论

**响应格式**:
```json
{
  "data": [
    {
      "commentid": "评论ID",
      "actid": "活动ID",
      "uid": 1000,
      "touid": null,
      "content": "这个活动看起来很有趣！",
      "likenum": 5,
      "replynum": 2,
      "createtime": "2025-10-16T12:00:00",
      "status": 1,
      "isLiked": false,
      "user": {
        "uid": 1000,
        "username": "用户1000",
        "profilepicture": "头像URL"
      },
      "touser": {
        "uid": 1001,
        "username": "用户1001",
        "profilepicture": "头像URL"
      }
    }
  ],
  "count": 10
}
```

**使用示例** (curl):
```bash
curl -X GET "http://localhost:5000/Activity/getCommentList?actid=act_123456&uid=1000"
```

---

### 2. 获取评论回复列表

**端点**: `GET /Activity/getReplyList`

**请求参数**:
- `commentid` (必填): 评论ID

**响应格式**:
```json
{
  "data": [
    {
      "replyid": "回复ID",
      "commentid": "评论ID",
      "actid": "活动ID",
      "uid": 2000,
      "touid": 1000,
      "content": "感谢关注！",
      "createtime": "2025-10-16T12:05:00",
      "status": 1,
      "user": {
        "uid": 2000,
        "username": "用户2000",
        "profilepicture": "头像URL"
      },
      "touser": {
        "uid": 1000,
        "username": "用户1000",
        "profilepicture": "头像URL"
      }
    }
  ],
  "count": 5
}
```

**使用示例** (curl):
```bash
curl -X GET "http://localhost:5000/Activity/getReplyList?commentid=comment_123456"
```

---

### 3. 获取新评论列表

**端点**: `POST /Activity/getNewCommentList`

**请求参数**:
```json
{
  "actid": "活动ID",
  "commentid": "评论ID (可选，获取此评论之后的新评论)"
}
```

**响应格式**:
```json
{
  "data": [
    {
      "type": "comment",
      "commentid": "评论ID",
      "actid": "活动ID",
      "uid": 1000,
      "content": "新评论内容",
      "likenum": 0,
      "replynum": 0,
      "createtime": "2025-10-16T12:10:00",
      "user": {
        "uid": 1000,
        "username": "用户1000",
        "profilepicture": "头像URL"
      }
    },
    {
      "type": "reply",
      "replyid": "回复ID",
      "commentid": "评论ID",
      "uid": 2000,
      "touid": 1000,
      "content": "新回复内容",
      "createtime": "2025-10-16T12:11:00",
      "user": {...},
      "touser": {...}
    }
  ],
  "count": 15
}
```

**使用示例** (curl):
```bash
curl -X POST http://localhost:5000/Activity/getNewCommentList \
  -H "Content-Type: application/json" \
  -d '{
    "actid": "act_123456",
    "commentid": "comment_123456"
  }'
```

---

### 4. 获取指定回复

**端点**: `GET /Activity/getReply`

**请求参数**:
- `replyid` (必填): 回复ID

**响应格式**:
```json
{
  "data": {
    "replyid": "回复ID",
    "commentid": "评论ID",
    "actid": "活动ID",
    "uid": 2000,
    "touid": 1000,
    "content": "回复内容",
    "createtime": "2025-10-16T12:05:00",
    "status": 1,
    "user": {
      "uid": 2000,
      "username": "用户2000",
      "profilepicture": "头像URL"
    },
    "touser": {
      "uid": 1000,
      "username": "用户1000",
      "profilepicture": "头像URL"
    }
  }
}
```

**使用示例** (curl):
```bash
curl -X GET "http://localhost:5000/Activity/getReply?replyid=reply_123456"
```

---

### 5. 获取评论回复列表（用户相关）

**端点**: `POST /Activity/getCommentReplyList`

**请求参数**:
```json
{
  "uid": 1000,
  "replyid": "回复ID (可选，获取此回复之后的回复)"
}
```

**响应格式**:
```json
{
  "data": [
    {
      "replyid": "回复ID",
      "commentid": "评论ID",
      "actid": "活动ID",
      "uid": 2000,
      "touid": 1000,
      "content": "回复内容",
      "createtime": "2025-10-16T12:05:00",
      "user": {...},
      "activity": {
        "actid": "活动ID",
        "content": "活动内容摘要",
        "coverimg": "封面图URL"
      }
    }
  ],
  "count": 8
}
```

**使用示例** (curl):
```bash
curl -X POST http://localhost:5000/Activity/getCommentReplyList \
  -H "Content-Type: application/json" \
  -d '{
    "uid": 1000
  }'
```

---

### 6. 评论点赞

**端点**: `POST /Activity/updateCommentLike`

**请求参数**:
```json
{
  "token": "用户认证令牌",
  "commentid": "评论ID",
  "uid": 1000,
  "likeuid": 2000,
  "actid": "活动ID"
}
```

**响应格式**:
```json
{
  "data": true
}
```

**使用示例** (curl):
```bash
curl -X POST http://localhost:5000/Activity/updateCommentLike \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "commentid": "comment_123456",
    "uid": 1000,
    "likeuid": 2000,
    "actid": "act_123456"
  }'
```

---

### 7. 取消评论点赞

**端点**: `POST /Activity/delCommentLike`

**请求参数**:
```json
{
  "token": "用户认证令牌",
  "commentid": "评论ID",
  "uid": 1000
}
```

**响应格式**:
```json
{
  "data": true
}
```

**使用示例** (curl):
```bash
curl -X POST http://localhost:5000/Activity/delCommentLike \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "commentid": "comment_123456",
    "uid": 1000
  }'
```

---

## 服务层方法

### CommentService 类方法

#### 1. add_comment(data)
添加活动评论

**参数**:
```python
data = {
    'actid': '活动ID',
    'uid': 1000,
    'touid': 1001,  # 可选
    'content': '评论内容'
}
```

**返回**: commentid (评论ID)

---

#### 2. add_comment_reply(data)
添加评论回复

**参数**:
```python
data = {
    'commentid': '评论ID',
    'actid': '活动ID',
    'uid': 2000,
    'touid': 1000,
    'content': '回复内容'
}
```

**返回**: replyid (回复ID)

---

#### 3. get_comment_list(actid, uid=None)
获取活动评论列表

**参数**:
- `actid`: 活动ID
- `uid`: 用户ID (可选，用于判断是否点赞)

**返回**: 评论列表 (包含用户信息)

---

#### 4. get_reply_list(commentid)
获取评论回复列表

**参数**:
- `commentid`: 评论ID

**返回**: 回复列表 (包含用户信息)

---

#### 5. get_reply(replyid)
获取指定回复

**参数**:
- `replyid`: 回复ID

**返回**: 回复对象 (包含用户信息)

---

#### 6. get_comment_reply_list(uid, replyid=None)
获取用户相关的回复列表

**参数**:
- `uid`: 用户ID
- `replyid`: 回复ID (可选)

**返回**: 回复列表 (包含活动信息)

---

#### 7. get_new_comment_list(actid, commentid=None)
获取新评论列表

**参数**:
- `actid`: 活动ID
- `commentid`: 评论ID (可选)

**返回**: 新评论和回复列表

---

#### 8. add_comment_like(commentid, uid, likeuid, actid)
评论点赞

**参数**:
- `commentid`: 评论ID
- `uid`: 点赞用户ID
- `likeuid`: 被点赞用户ID
- `actid`: 活动ID

**返回**: bool (是否成功)

---

#### 9. remove_comment_like(commentid, uid)
取消评论点赞

**参数**:
- `commentid`: 评论ID
- `uid`: 用户ID

**返回**: bool (是否成功)

---

#### 10. delete_comment(commentid, uid)
删除评论 (软删除)

**参数**:
- `commentid`: 评论ID
- `uid`: 用户ID (验证权限)

**返回**: bool (是否成功)

---

#### 11. delete_reply(replyid, uid)
删除回复 (软删除)

**参数**:
- `replyid`: 回复ID
- `uid`: 用户ID (验证权限)

**返回**: bool (是否成功)

---

## 特性说明

### 1. 评论系统
- **层级结构**: 评论 → 回复
- **软删除**: 评论和回复支持软删除，不会物理删除数据
- **点赞功能**: 支持对评论点赞，防止重复点赞
- **回复功能**: 支持对评论进行回复，支持 @用户

### 2. 用户信息
- 每条评论和回复都包含用户信息（默认值）
- 支持显示被回复用户信息
- 用户信息包含：uid, username, profilepicture

### 3. 计数管理
- 自动更新活动的评论数
- 自动更新评论的回复数和点赞数
- 删除时自动减少计数

### 4. 查询优化
- 评论按创建时间倒序排列（最新的在前）
- 回复按创建时间正序排列（最早的在前）
- 使用索引优化查询性能

## 测试数据

系统已包含测试数据:
- **10 条评论**: 分布在 3 个活动中
- **6 条回复**: 不同用户的互动回复
- **9 个点赞**: 用户对评论的点赞

### 活动评论分布:
- 深圳周末户外徒步活动: 3 评论, 2 回复
- 深圳湾骑行活动: 4 评论, 2 回复
- 南山科技园周末羽毛球活动: 3 评论, 2 回复

## 使用建议

### 前端集成
1. 在活动详情页显示评论列表
2. 实现评论输入框，支持 @用户
3. 显示评论回复，支持展开/折叠
4. 实现点赞功能，显示点赞数和点赞状态
5. 支持下拉刷新获取新评论

### 性能优化
1. 评论列表分页加载
2. 回复列表按需加载（点击展开）
3. 对 `actid` 和 `commentid` 字段建立索引
4. 使用缓存减少数据库查询

### 数据验证
1. 评论内容不能为空
2. 验证用户权限（删除时）
3. 防止重复点赞
4. 验证 actid 和 commentid 的有效性

## 相关文档
- [Activity 模块主文档](README.md)
- [API 接口文档](community_api.md)
- [数据库表结构](community_cacheTable.md)

---

**版本**: 1.0.0  
**最后更新**: 2025-10-16  
**维护者**: Development Team

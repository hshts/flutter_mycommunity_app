# /Activity/getCommentList 接口文档

## 接口信息

**端点**: `GET /Activity/getCommentList`  
**方法**: GET  
**功能**: 获取指定活动的评论列表  
**状态**: ✅ 已实现并测试通过

---

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| actid  | string | 是 | 活动ID |
| uid    | integer | 否 | 用户ID，用于判断用户是否点赞过评论 |

### 请求示例

```bash
# 不带 uid 参数
GET /Activity/getCommentList?actid=act_2ab8038990224589

# 带 uid 参数（显示用户点赞状态）
GET /Activity/getCommentList?actid=act_2ab8038990224589&uid=1000
```

---

## 响应格式

### 成功响应 (200 OK)

```json
{
  "data": [
    {
      "commentid": "29c3bc37-34f2-4819-83ea-ee135248871b",
      "actid": "act_2ab8038990224589",
      "uid": 1002,
      "touid": null,
      "content": "有什么要求吗？新人可以参加吗？",
      "likenum": 1,
      "replynum": 0,
      "createtime": "2025-10-16T12:04:29.509041",
      "status": 1,
      "isLiked": false,
      "user": {
        "uid": 1002,
        "username": "用户1002",
        "profilepicture": "https://via.placeholder.com/100"
      }
    }
  ],
  "count": 3
}
```

### 响应字段说明

#### 根对象

| 字段 | 类型 | 说明 |
|------|------|------|
| data | array | 评论对象数组 |
| count | integer | 评论总数 |

#### Comment 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| commentid | string | 评论ID (UUID) |
| actid | string | 活动ID |
| uid | integer | 评论用户ID |
| touid | integer/null | 目标用户ID (回复某人时) |
| content | string | 评论内容 |
| likenum | integer | 点赞数 |
| replynum | integer | 回复数 |
| createtime | string | 创建时间 (ISO格式) |
| status | integer | 状态 (1: 正常, 0: 已删除) |
| isLiked | boolean | 当前用户是否点赞 (仅当提供uid时) |
| user | object | 评论用户信息 |
| touser | object | 目标用户信息 (仅当touid不为空时) |

#### User 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| uid | integer | 用户ID |
| username | string | 用户名 |
| profilepicture | string | 用户头像URL |

---

## 错误响应

### 缺少必填参数 (400 Bad Request)

```json
{
  "error": "Missing actid parameter"
}
```

### 服务器错误 (500 Internal Server Error)

```json
{
  "error": "错误详细信息"
}
```

---

## 使用示例

### cURL 示例

```bash
# 基本请求
curl -X GET "http://localhost:5000/Activity/getCommentList?actid=act_2ab8038990224589"

# 带用户ID的请求
curl -X GET "http://localhost:5000/Activity/getCommentList?actid=act_2ab8038990224589&uid=1000"
```

### Python 示例

```python
import requests

# 基本请求
response = requests.get(
    'http://localhost:5000/Activity/getCommentList',
    params={'actid': 'act_2ab8038990224589'}
)
data = response.json()
print(f"评论数: {data['count']}")

# 带用户ID的请求
response = requests.get(
    'http://localhost:5000/Activity/getCommentList',
    params={
        'actid': 'act_2ab8038990224589',
        'uid': 1000
    }
)
data = response.json()

for comment in data['data']:
    print(f"用户{comment['uid']}: {comment['content']}")
    print(f"  点赞: {comment['likenum']}, 回复: {comment['replynum']}")
    print(f"  已点赞: {comment['isLiked']}")
```

### JavaScript/Fetch 示例

```javascript
// 基本请求
fetch('http://localhost:5000/Activity/getCommentList?actid=act_2ab8038990224589')
  .then(response => response.json())
  .then(data => {
    console.log(`评论数: ${data.count}`);
    data.data.forEach(comment => {
      console.log(`${comment.user.username}: ${comment.content}`);
    });
  });

// 带用户ID的请求
const actid = 'act_2ab8038990224589';
const uid = 1000;
fetch(`http://localhost:5000/Activity/getCommentList?actid=${actid}&uid=${uid}`)
  .then(response => response.json())
  .then(data => {
    data.data.forEach(comment => {
      const likedStatus = comment.isLiked ? '已点赞' : '未点赞';
      console.log(`${comment.content} - ${likedStatus}`);
    });
  });
```

### Flutter/Dart 示例

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> getCommentList(String actid, {int? uid}) async {
  final queryParams = {
    'actid': actid,
    if (uid != null) 'uid': uid.toString(),
  };
  
  final uri = Uri.http(
    'localhost:5000',
    '/Activity/getCommentList',
    queryParams,
  );
  
  final response = await http.get(uri);
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    print('评论数: ${data['count']}');
    
    for (var comment in data['data']) {
      print('${comment['user']['username']}: ${comment['content']}');
      print('  点赞: ${comment['likenum']}, 回复: ${comment['replynum']}');
      if (comment.containsKey('isLiked')) {
        print('  已点赞: ${comment['isLiked']}');
      }
    }
  }
}

// 使用示例
void main() {
  // 不带uid
  getCommentList('act_2ab8038990224589');
  
  // 带uid
  getCommentList('act_2ab8038990224589', uid: 1000);
}
```

---

## 业务逻辑

### 查询逻辑

1. 根据 `actid` 查询该活动的所有评论
2. 只返回状态为 1 (正常) 的评论
3. 按创建时间倒序排列（最新的在前）
4. 为每条评论附加用户信息
5. 如果提供了 `uid`，判断用户是否点赞过该评论

### 排序规则

- **评论**: 按 `createtime` 降序（最新的在最前面）
- **回复**: 按 `createtime` 升序（最早的在最前面）

### 用户信息

评论中的用户信息目前使用默认值:
```json
{
  "uid": 1002,
  "username": "用户1002",
  "profilepicture": "https://via.placeholder.com/100"
}
```

> **注意**: 在生产环境中，应该从用户表中查询真实的用户信息。

---

## 性能考虑

### 查询优化

- 在 `actid` 字段上建立索引
- 在 `status` 字段上建立索引
- 使用复合索引 `(actid, status)`

### 建议的索引

```sql
CREATE INDEX idx_activity_comments_actid ON activity_comments(actid);
CREATE INDEX idx_activity_comments_status ON activity_comments(status);
CREATE INDEX idx_activity_comments_actid_status ON activity_comments(actid, status);
```

### 分页建议

当评论数量较大时，建议添加分页功能：

```python
# 建议添加的参数
page = request.args.get('page', 1, type=int)
page_size = request.args.get('page_size', 20, type=int)

comments = ActivityComment.query.filter_by(
    actid=actid,
    status=1
).order_by(ActivityComment.createtime.desc())\
 .paginate(page=page, per_page=page_size)
```

---

## 测试数据

### 当前测试数据统计

- **总评论数**: 10
- **总回复数**: 6
- **总点赞数**: 9

### 测试活动

| 活动 | 评论数 | 回复数 |
|------|--------|--------|
| 深圳周末户外徒步活动 | 3 | 2 |
| 深圳湾骑行活动 | 4 | 2 |
| 南山科技园周末羽毛球活动 | 3 | 2 |

---

## 相关接口

### 评论相关接口

1. **GET /Activity/getCommentList** - 获取活动评论列表 ✅
2. **POST /Activity/updatecomment** - 发布活动评论 ✅
3. **POST /Activity/delcomment** - 删除活动评论 ✅
4. **GET /Activity/getReplyList** - 获取评论回复列表 ✅
5. **POST /Activity/updateCommentLike** - 评论点赞 ✅
6. **POST /Activity/delCommentLike** - 取消评论点赞 ✅
7. **POST /Activity/getNewCommentList** - 获取新评论列表 ✅
8. **GET /Activity/getReply** - 获取指定回复 ✅
9. **POST /Activity/getCommentReplyList** - 获取用户相关回复 ✅

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2025-10-16 | 初始版本，完整实现评论列表接口 |

---

## 注意事项

1. **权限验证**: 当前接口未启用 token 验证，生产环境建议添加
2. **数据量**: 建议添加分页功能，避免一次返回过多数据
3. **用户信息**: 当前使用模拟数据，需要集成真实的用户系统
4. **缓存**: 对于热门活动的评论，建议添加缓存机制
5. **敏感词**: 建议添加敏感词过滤功能

---

## 联系方式

如有问题或建议，请联系开发团队。

**文档版本**: 1.0.0  
**最后更新**: 2025-10-16  
**维护者**: Development Team

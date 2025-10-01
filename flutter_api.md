# Flutter前端社交电商模块 API 接口清单

本文件基于 lib/service 目录下所有 Dart 服务模块，按模块分组，列举所有请求接口，包含接口路径、请求方式、主要输入参数、输出字段及注释说明。

---

## 1. 用户服务模块（userservice.dart）

| 接口 | 方法 | 输入参数 | 输出字段 | 说明 |
|------|------|---------|---------|------|
| /user/register | POST | username, email, phone, password, nickname | user对象, token | 用户注册 |
| /user/login | POST | login_type, identifier, password/verification_code | user对象, token | 用户登录（支持手机号/邮箱/验证码/密码） |
| /user/info | GET | uid, token | user对象 | 获取用户信息 |
| /user/update | POST | uid, nickname, avatar, gender, birthday, location | user对象 | 更新用户信息 |
| /user/change_password | POST | uid, old_password, new_password | 无 | 修改密码 |
| /user/send_verification_code | POST | contact, contact_type | 无 | 发送验证码（手机/邮箱） |
| /user/reset_password | POST | contact, contact_type, verification_code, new_password | 无 | 重置密码 |
| /user/list | GET | page, per_page, search | items[], total | 获取用户列表（管理员） |
| /user/update_status | POST | uid, status | 无 | 更新用户状态（管理员） |

---

## 2. 团购活动服务模块（activity.dart）

| 接口 | 方法 | 输入参数 | 输出字段 | 说明 |
|------|------|---------|---------|------|
| /activity/create | POST | title, desc, image_url, activity_type, start_time, end_time, min_people, max_people, original_price, group_price, creator_id | activity对象 | 创建团购活动 |
| /activity/join | POST | actid, uid, username, sex | activity对象 | 参与团购活动 |
| /activity/list | GET | goodpriceid | items[] | 获取活动列表（可按商品筛选） |
| /activity/clientPaySuccess | POST | orderid, uid | 无 | 客户端支付成功通知 |

---

## 3. 商品/团购服务模块（gpservice.dart）

| 接口 | 方法 | 输入参数 | 输出字段 | 说明 |
|------|------|---------|---------|------|
| /grouppurchase/hotsearchProduct | GET | 无 | items[] | 获取热门搜索关键词 |
| /grouppurchase/getRecommendSearchProduct | POST | content | items[] | 推荐搜索关键词 |
| /grouppurchase/searchProduct | POST | content, ordertype, citycode, currentIndex, isAllCity | items[], pagination | 搜索商品 |
| /grouppurchase/getGoodPriceInfo | GET | goodpriceid | goodPrice对象 | 获取商品详情 |
| /grouppurchase/getRecommendGoodPriceList | GET | type, currentIndex, citycode | items[], pagination | 推荐商品列表 |
| /grouppurchase/updateGoodPriceCollection | POST | goodpriceid, uid, token | 无 | 收藏商品 |
| /grouppurchase/delGoodPriceCollection | POST | goodpriceid, uid, token | 无 | 取消收藏 |
| /grouppurchase/getUserGoodPriceCollectionInfo | GET | currentIndex, uid, token | items[], pagination | 获取用户收藏商品列表 |
| /grouppurchase/updatecomment | POST | goodpriceid, uid, touid, content, commentid, token | commentid | 添加评论/回复 |
| /grouppurchase/getcomment | GET | goodpriceid, uid | items[] | 获取评论列表 |
| /grouppurchase/delcomment | POST | commentid, replyid, uid, goodpriceid, token | 无 | 删除评论/回复 |
| /grouppurchase/updateCommentLike | POST | commentid, uid, goodpriceid, token | 无 | 点赞评论 |
| /grouppurchase/delCommentLike | POST | commentid, uid, token | 无 | 取消评论点赞 |
| /grouppurchase/updateGoodPriceLike | POST | goodpriceid, uid, token | 无 | 商品点赞 |
| /grouppurchase/updateCancelLike | POST | goodpriceid, uid, token | 无 | 取消商品点赞 |
| /grouppurchase/createGoodPrice | POST | title, content, price, originalprice, pic, category, province, city, purchasechannels, producturl, uid, token | goodpriceid | 创建商品 |
| /grouppurchase/getMyGoodPricePendingList | GET | uid, token | items[] | 我的待审核商品 |
| /grouppurchase/getMyGoodPriceFinishList | GET | uid, token | items[] | 我的已审核商品 |
| /grouppurchase/delMyGoodPrice | GET | goodpriceid, uid, token | 无 | 删除我的商品 |

---

## 4. 即时通讯服务模块（imservice.dart）

| 接口 | 方法 | 输入参数 | 输出字段 | 说明 |
|------|------|---------|---------|------|
| /im/send | POST | sender_id, receiver_id, content, msg_type | msg对象 | 发送消息 |
| /im/conversation_list | GET | uid | items[] | 获取会话列表 |
| /im/unread_count | GET | uid | unread_count | 获取未读消息数 |

---

## 5. 阿里云服务模块（aliyun.dart）

| 接口 | 方法 | 输入参数 | 输出字段 | 说明 |
|------|------|---------|---------|------|
| /aliyun/send_sms | POST | phone, code | 无 | 发送短信验证码 |
| /aliyun/send_email | POST | email, code | 无 | 发送邮件验证码 |
| /aliyun/upload_oss | POST | file | url | OSS文件上传 |

---

## 字段注释说明

- 所有接口均返回统一响应格式：
```
{
  "code": 200,
  "message": "操作成功",
  "success": true,
  "data": ...
}
```
- 输入参数与前端 service/model 字段完全一致。
- 输出字段结构与 model.dart 对齐，如 user对象、goodPrice对象、activity对象、msg对象等。
- 认证接口需传递 token（Authorization header 或参数）。
- 分页接口包含 pagination 字段：page, per_page, total, pages, has_prev, has_next。
- 详细字段结构请参考前端 model 相关定义。

# Flutter社区应用模型类文档

## 1. Activity 活动模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actid | String | 活动ID |
| members | List<User>? | 活动成员列表 |
| peoplenum | int? | 活动人数 |
| createtime | String? | 创建时间 |
| updatetime | String? | 更新时间 |
| content | String | 活动内容 |
| score | String? | 活动评分 |
| actimagespath | String? | 活动图片路径 |
| status | int? | 活动状态 |
| user | User? | 活动发起用户 |
| actcity | String? | 活动城市 |
| actprovince | String? | 活动省份 |
| coverimg | String? | 封面图片 |
| coverimgwh | String | 封面图片宽高比 |
| likenum | int | 点赞数 |
| collectionnum | int | 收藏数 |
| startyear | int? | 开始年份 |
| endyear | int? | 结束年份 |
| commentnum | int? | 评论数 |
| currentpeoplenum | int? | 当前参与人数 |
| maxcost | double | 最大费用 |
| mincost | double | 最小费用 |
| address | String? | 活动地址 |
| addresstitle | String? | 地址标题 |
| lat | double? | 纬度坐标 |
| lng | double? | 经度坐标 |
| paytype | int? | 支付类型(0免费 1后付款 2先付款团购) |
| goodpriceid | String? | 商品ID |
| activityEvaluate | ActivityEvaluate? | 活动评价 |
| joinnum | int? | 参与人数 |
| viewnum | int? | 浏览数 |
| orderid | String? | 订单ID |
| locked | int? | 是否已锁定(活动开始) |
| goodPiceModel | GoodPiceModel? | 商品模型 |

## 2. ActivityEvaluate 活动评价模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actevaluateid | int? | 活动评价ID |
| activity | Activity? | 关联的活动 |
| createtime | String? | 创建时间 |
| evaluatestatus | int? | 评价状态 |

## 3. EvaluateActivity 活动评价详情模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| evaluateid | int? | 评价ID |
| actid | String? | 活动ID |
| user | User? | 评价用户 |
| touid | int? | 被评价用户ID |
| content | String? | 评价内容 |
| imagepaths | String? | 图片路径 |
| liketype | int? | 点赞类型 |
| likenum | int? | 点赞数 |
| likeuid | int? | 点赞用户ID |
| createtime | String? | 创建时间 |
| actcontent | String? | 活动内容 |
| coverimg | String? | 封面图片 |
| replys | List<EvaluateActivityReply>? | 回复列表 |
| replynum | int? | 回复数 |
| orderid | String | 订单ID |
| goodpriceid | String | 商品ID |

## 4. EvaluateActivityReply 活动评价回复模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| replyid | int? | 回复ID |
| actid | String? | 活动ID |
| evaluateid | int? | 评价ID |
| replyuser | User? | 回复用户 |
| touser | User? | 被回复用户 |
| replycontent | String? | 回复内容 |
| replycreatetime | String? | 回复创建时间 |
| isread | bool? | 是否已读 |
| type | String? | 回复类型 |
| ismaster | bool? | 是否是楼主 |
| actcontent | String? | 活动内容 |
| coverimg | String? | 封面图片 |
| imagepaths | String? | 图片路径 |

## 5. Comment 评论模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| commentid | int? | 评论ID |
| actid | String? | 活动ID |
| user | User? | 评论用户 |
| content | String? | 评论内容 |
| likenum | int? | 点赞数 |
| createtime | String? | 创建时间 |
| replys | List<CommentReply>? | 回复列表 |
| likeuid | int | 点赞用户ID |

## 6. CommentReply 评论回复模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| replyid | int? | 回复ID |
| actid | String? | 活动ID |
| commentid | int? | 评论ID |
| evaluateid | int? | 评价ID |
| replyuser | User? | 回复用户 |
| touser | User? | 被回复用户 |
| replycontent | String? | 回复内容 |
| replycreatetime | String? | 回复创建时间 |
| isread | bool? | 是否已读 |
| type | String? | 回复类型 |
| ismaster | bool? | 是否是楼主 |
| actcontent | String? | 活动内容 |
| coverimg | String? | 封面图片 |
| imagepaths | String? | 图片路径 |

## 7. User 用户模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | int | 用户ID |
| mobile | String | 手机号 |
| username | String | 用户名 |
| email | String | 邮箱 |
| sex | String? | 性别 |
| country | String? | 国家 |
| province | String? | 省份 |
| city | String? | 城市 |
| signature | String | 个人签名 |
| profilepicture | String? | 头像 |
| pwerrorcount | int? | 密码错误次数 |
| birthday | String? | 生日 |
| followers | int? | 粉丝数 |
| following | int? | 关注数 |
| isFollow | bool | 是否已关注 |
| updatetime | String? | 更新时间 |
| likenum | int? | 点赞数 |
| token | String? | 认证令牌 |
| likeact | int? | 活动点赞数 |
| collectionact | int? | 活动收藏数 |
| likecomment | int | 评论点赞数 |
| likeevaluate | int? | 评价点赞数 |
| collectionproduct | int? | 商品收藏数 |
| aliuserid | String | 支付宝用户ID |
| wxuserid | String | 微信用户ID |
| iosuserid | String | iOS用户ID |
| likebug | int | BUG点赞数 |
| likesuggest | int | 建议点赞数 |
| likebugcomment | int | BUG评论点赞数 |
| likesuggestcomment | int | 建议评论点赞数 |
| likemoment | int | 动态点赞数 |
| likemomentcomment | int | 动态评论点赞数 |
| likegoodpricecomment | int | 商品评论点赞数 |
| notinteresteduids | String? | 不感兴趣的用户 |
| blacklist | String? | 黑名单 |
| goodpricenotinteresteduids | String? | 不感兴趣的商品用户 |
| usertype | int? | 用户类型 |
| interest | String? | 兴趣 |
| voice | String? | 语音 |
| isNew | bool? | 是否新用户 |
| business | int | 是否商户 |
| subject | String | 关注主题 |

## 8. Like 点赞模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| likeid | int? | 点赞ID |
| liketype | int? | 点赞类型(0活动 1留言 2评价 3bug 4建议) |
| contentid | String? | 内容ID |
| user | User? | 点赞用户 |
| touid | int? | 被点赞用户ID |
| createtime | String? | 创建时间 |

## 9. Order 订单模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| orderid | String? | 订单ID |
| gpactid | String? | 团购活动ID |
| gpprice | double? | 团购价格 |
| uid | int? | 用户ID |
| createtime | String? | 创建时间 |
| updatetime | String? | 更新时间 |
| paymenttype | int? | 支付类型 |
| goodpriceid | String | 商品ID |
| goodpricesku | String | 商品SKU |
| goodpricebrand | String | 商品品牌 |
| productname | String? | 商品名称 |
| productpic | String? | 商品图片 |
| creategpuid | int? | 团购发起人ID |
| specsid | int? | 规格ID |
| user | User? | 用户 |
| activity | Activity? | 活动 |
| ordertype | int? | 订单类型(0拼玩订单 3团购订单) |
| orderstatus | int? | 订单状态(0待付款 1已付款 2已退款 3已转账) |
| productnum | int | 商品数量 |
| expirestime | int? | 超时时间(秒) |
| goodpricetitle | String | 商品标题 |
| goodpricepic | String | 商品图片 |
| touid | int | 目标用户ID |
| goodpricespeacename | String | 商品规格名称 |

## 10. Follow 关注模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | int? | ID |
| uid | int? | 用户ID |
| fans | int? | 粉丝ID |
| username | String? | 用户名 |
| profilepicture | String? | 头像 |
| isread | int? | 是否已读 |
| createtime | String? | 创建时间 |
| type | int? | 类型(0关注 1点赞) |

## 11. Report 举报模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| reportid | String? | 举报ID |
| uid | int? | 用户ID |
| actid | String | 活动ID |
| createtime | String | 创建时间 |
| updatetime | String | 更新时间 |
| repleycontent | String | 回复内容 |
| reporttype | int | 举报类型(0疑似欺诈 1低俗图片 2其他) |
| sourcetype | int? | 来源类型(0活动 1商品 2用户) |
| activity | Activity? | 活动 |
| goodPiceModel | GoodPiceModel? | 商品模型 |
| user | User? | 用户 |

## 12. Dynamic 动态模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | int | ID |
| uid | int | 用户ID |
| actiontype | String | 动作类型 |
| actiondata | String | 动作数据 |
| createtime | String | 创建时间 |

## 13. GoodPiceModel 商品模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| goodpriceid | String | 商品ID |
| title | String | 标题 |
| content | String | 内容 |
| category | int | 分类 |
| brand | String | 品牌 |
| discount | double | 折扣 |
| endtime | String | 结束时间 |
| createtime | String | 创建时间 |
| albumpics | String | 相册图片 |
| pic | String | 图片 |
| sellnum | int | 销售数量 |
| collectionnum | int | 收藏数量 |
| province | String | 省份 |
| city | String | 城市 |
| uid | int | 用户ID |
| username | String | 用户名 |
| profilepicture | String | 用户头像 |
| likenum | int | 点赞数 |
| unlikenum | int | 不喜欢数 |
| commentnum | int | 评论数 |
| productstatus | int | 商品状态(0未审核 1已审核 2退回 3已过期) |
| satisfactionrate | double | 满意度 |
| activitycount | int | 活动数 |
| tag | String | 标签 |
| msg | String | 消息 |
| addresstitle | String | 地址标题 |
| address | String | 地址 |
| lat | double | 纬度 |
| lng | double | 经度 |
| mincost | double | 最小费用 |
| maxcost | double | 最大费用 |
| evaluatenum | int | 评价数 |

## 14. Skuspecs 商品规格模型

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| specsid | String | 规格ID |
| goodpriceid | String | 商品ID |
| spdata | String | 规格数据 |
| cost | double | 费用 |
| pic | String | 图片 |
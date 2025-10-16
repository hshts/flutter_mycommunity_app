# 社区应用API接口文档

## 1. 模块概述

该文档详细描述了社区应用各模块的API接口，包括Activity(活动)、Group Purchase(团购)、User(用户)和IM(即时通讯)等核心模块。每个接口都包含请求路径、方法、输入参数和输出结果的详细说明。

## 2. Activity模块 (活动相关)

### 2.1 创建活动
- **接口**: `/Activity/createActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - province, city: 省市信息
  - uid: 用户ID
  - content: 活动内容
  - actimagespath: 活动图片路径列表
  - coverimg: 封面图片
  - coverimgWH: 封面图片宽高比
  - startyear, endyear: 活动起止时间
  - ispublic: 是否公开
  - address, addresstitle: 地址信息
  - lat, lng: 经纬度
  - paytype: 支付类型
  - goodpriceid: 商品ID（可选）
  - captchaVerification: 验证码验证信息
- **输出**: Activity对象

### 2.2 获取活动详情
- **接口**: `/Activity/getActivity`
- **方法**: GET
- **输入参数**:
  - actid: 活动ID
  - uid: 用户ID（可选）
- **输出**: Activity对象

### 2.3 获取活动列表（按更新时间）
- **接口**: `/Activity/getActivityListByUpdateTime`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - citycode: 城市代码
- **输出**: Activity对象列表

### 2.4 获取用户活动列表
- **接口**: `/Activity/getActivityListByUser`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.5 获取用户参与的活动列表
- **接口**: `/Activity/getJoinActivityListByUser`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: Activity对象列表

### 2.6 活动点赞
- **接口**: `/Activity/updateLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.7 活动取消点赞
- **接口**: `/Activity/delLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.8 活动收藏
- **接口**: `/Activity/updateCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.9 活动取消收藏
- **接口**: `/Activity/delCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.10 发布活动评论
- **接口**: `/Activity/updatecomment`
- **方法**: POST
- **输入参数**:
  - commentid: 评论ID（回复时使用）
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 评论内容
  - captchaVerification: 验证码验证信息
- **输出**: 评论ID

### 2.11 删除活动评论
- **接口**: `/Activity/delcomment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - replyid: 回复ID（删除回复时使用）
  - actid: 活动ID
- **输出**: 操作结果（布尔值）

### 2.12 评论点赞
- **接口**: `/Activity/updateCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - actid: 活动ID
- **输出**: 操作结果（布尔值）

### 2.13 评价点赞
- **接口**: `/Activity/updateEvaluateLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - evaluateid: 评价ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - actid: 活动ID
- **输出**: 操作结果（布尔值）

### 2.14 参加活动
- **接口**: `/Activity/joinActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - username: 用户名
  - sex: 性别
- **输出**: GroupRelation对象

### 2.15 删除活动
- **接口**: `/Activity/delActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.16 搜索活动
- **接口**: `/Activity/searchActivity`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
  - ordertype: 排序类型
  - citycode: 城市代码
  - currentIndex: 当前索引
  - isAllCity: 是否所有城市
- **输出**: Activity对象列表

### 2.17 获取活动成员信息
- **接口**: `/Activity/getActivityMember`
- **方法**: GET
- **输入参数**:
  - actid: 活动ID
  - uid: 用户ID
- **输出**: Activity对象

### 2.18 获取活动和待支付订单信息
- **接口**: `/Activity/getActivityAndPendingOrder`
- **方法**: GET
- **输入参数**:
  - actid: 活动ID
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: Activity对象

### 2.19 获取用户前5个活动列表
- **接口**: `/Activity/getActivityListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.20 获取所有用户前5个活动列表
- **接口**: `/Activity/getAllActivityListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.21 获取用户前5个已完成活动列表
- **接口**: `/Activity/getActivityFinishListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.22 获取用户参与的前5个活动列表
- **接口**: `/Activity/getJoinActivityListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.23 获取用户参与的所有前5个活动列表
- **接口**: `/Activity/getALLJoinActivityListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.24 获取用户收藏的前5个活动列表
- **接口**: `/Activity/getCollectionActivityListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.25 根据城市获取活动列表
- **接口**: `/Activity/getActivityListByCity`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - citycode: 城市代码
- **输出**: Activity对象列表

### 2.26 根据关注用户获取活动列表
- **接口**: `/Activity/getActivityFollowList`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.27 根据社团ID获取活动列表
- **接口**: `/Activity/selectActivityByCid`
- **方法**: GET
- **输入参数**:
  - cid: 社团ID
- **输出**: Activity对象列表

### 2.28 取消评价点赞
- **接口**: `/Activity/delEvaluateLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - evaluateid: 评价ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - actid: 活动ID
- **输出**: 操作结果（布尔值）

### 2.29 更新活动时间
- **接口**: `/Activity/updateActivityTime`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - startyear: 开始年份
  - endyear: 结束年份
- **输出**: 操作结果（布尔值）

### 2.30 更新活动信息
- **接口**: `/Activity/updateActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - content: 活动内容
  - actimagespath: 活动图片路径列表
  - coverimg: 封面图片
  - coverimgWH: 封面图片宽高比
  - ispublic: 是否公开
  - address: 地址
  - addresstitle: 地址标题
  - lat: 纬度
  - lng: 经度
  - captchaVerification: 验证码验证信息
- **输出**: 操作结果（布尔值）

### 2.31 更新活动状态
- **接口**: `/Activity/updateActivityStatus`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - status: 状态
- **输出**: 操作结果（布尔值）

### 2.32 更新活动结束状态
- **接口**: `/Activity/updateActivityStatusEnd`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.33 退出活动
- **接口**: `/Activity/exitActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 退出结果码

### 2.34 获取群聊信息
- **接口**: `/Activity/getGroupConversation`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - timeline_id: 时间线ID
  - uid: 用户ID
- **输出**: GroupRelation对象

### 2.35 同步用户通知
- **接口**: `/Activity/syncUserNotice`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: UserNotice对象

### 2.36 获取活动点赞列表
- **接口**: `/Activity/getActivityLikeList`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - likeid: 点赞ID
- **输出**: Like对象列表

### 2.37 获取活动评论列表
- **接口**: `/Activity/getCommentList`
- **方法**: GET
- **输入参数**:
  - actid: 活动ID
  - uid: 用户ID
- **输出**: Comment对象列表

### 2.38 获取评论回复列表
- **接口**: `/Activity/getReplyList`
- **方法**: GET
- **输入参数**:
  - commentid: 评论ID
- **输出**: CommentReply对象列表

### 2.39 获取新评论列表
- **接口**: `/Activity/getNewCommentList`
- **方法**: POST
- **输入参数**:
  - actid: 活动ID
  - commentid: 评论ID
- **输出**: CommentReply对象列表

### 2.40 获取系统通知
- **接口**: `/Activity/getSysNotice`
- **方法**: POST
- **输入参数**: 无
- **输出**: CommentReply对象列表

### 2.41 获取未评价订单列表
- **接口**: `/Activity/getUnEvaluateOrderList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: Order对象列表

### 2.42 同步活动关系初始化
- **接口**: `/Activity/listActivityGroupConversationsInit`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 2.43 搜索活动推荐
- **接口**: `/Activity/getRecommendSearchActivity`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
- **输出**: SearchResult对象列表

### 2.44 热门活动搜索
- **接口**: `/Activity/hotsearchActivity`
- **方法**: POST
- **输入参数**: 无
- **输出**: SearchResult对象列表

### 2.45 搜索更多类似活动
- **接口**: `/Activity/searchMoreLikeActivity`
- **方法**: POST
- **输入参数**:
  - actid: 活动ID
  - currentIndex: 当前索引
- **输出**: Activity对象列表

### 2.46 标记消息已读
- **接口**: `/Activity/postReadMessage`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - msgtype: 消息类型
- **输出**: 操作结果（布尔值）

### 2.47 标记点赞已读
- **接口**: `/Activity/postReadLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - liketype: 点赞类型
- **输出**: 操作结果（布尔值）

### 2.48 评价活动
- **接口**: `/Activity/evaluateActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - content: 评价内容
  - images: 图片列表
  - captchaVerification: 验证码验证信息
- **输出**: 操作结果（布尔值）

### 2.49 回复评价
- **接口**: `/Activity/evaluateReply`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - evaluateid: 评价ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 回复内容
  - captchaVerification: 验证码验证信息
- **输出**: 操作结果（布尔值）

### 2.50 退出并删除活动
- **接口**: `/Activity/delQuiteActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.51 删除活动订单
- **接口**: `/Activity/delActivityOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - orderid: 订单ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.52 退款活动订单
- **接口**: `/Activity/refundActivityOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - orderid: 订单ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.53 管理员删除并退出活动
- **接口**: `/Activity/manageDelQuiteActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - memberid: 成员ID
- **输出**: 操作结果（布尔值）

### 2.54 活动资金转账
- **接口**: `/Activity/activityFundTransfer`
- **方法**: POST
- **输入参数**:
  - actid: 活动ID
  - token: 用户认证令牌
  - uid: 用户ID
  - orderid: 订单ID
- **输出**: 操作结果（布尔值）

### 2.55 获取评价活动列表
- **接口**: `/Activity/getEvaluateActivity`
- **方法**: POST
- **输入参数**:
  - actid: 活动ID
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: EvaluateActivity对象列表

### 2.56 获取评价回复列表
- **接口**: `/Activity/getEvaluateReplyList`
- **方法**: POST
- **输入参数**:
  - evaluateid: 评价ID
- **输出**: EvaluateActivityReply对象列表

### 2.57 根据评价ID获取评价活动信息
- **接口**: `/Activity/getEvaluateActivityByEvaluateid`
- **方法**: POST
- **输入参数**:
  - evaluateid: 评价ID
- **输出**: EvaluateActivity对象

### 2.58 更新支付宝信息
- **接口**: `/Activity/updateAliPayInfo`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - realname: 真实姓名
  - idcardno: 身份证号
  - cardno: 银行卡号
  - captchaVerification: 验证码验证信息
- **输出**: 订单信息

### 2.59 举报活动
- **接口**: `/Activity/reportActivity`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - touid: 目标用户ID
  - token: 用户认证令牌
  - actid: 活动ID
  - reporttype: 举报类型
  - reportcontent: 举报内容
  - images: 图片列表
  - imagetype: 图片类型
  - sourcetype: 来源类型
  - captchaVerification: 验证码验证信息
- **输出**: 举报ID

### 2.60 获取指定回复
- **接口**: `/Activity/getReply`
- **方法**: GET
- **输入参数**:
  - replyid: 回复ID
- **输出**: CommentReply对象

### 2.61 获取评论回复列表
- **接口**: `/Activity/getCommentReplyList`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - replyid: 回复ID
- **输出**: CommentReply对象列表

### 2.62 获取用户活动待付款订单
- **接口**: `/Activity/getActivityPendingOrder`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - actid: 活动ID
- **输出**: Order对象

### 2.63 获取我的举报
- **接口**: `/Activity/getMyReport`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: Report对象列表

### 2.64 获取我的举报详情
- **接口**: `/Activity/getMyReportInfo`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - reportid: 举报ID
  - sourcetype: 来源类型
- **输出**: Report对象

### 2.65 客户端支付成功通知
- **接口**: `/Activity/clientPaySuccess`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - orderid: 订单ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 2.66 获取用户点赞活动列表
- **接口**: `/Activity/getUserLikeActivityList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: Activity对象列表

### 2.67 获取用户收藏活动列表
- **接口**: `/Activity/getUserCollectionActivityList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: Activity对象列表

### 2.68 获取用户评价活动列表
- **接口**: `/Activity/getUserEvaluateActivityList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: EvaluateActivity对象列表

### 2.69 获取用户评论活动列表
- **接口**: `/Activity/getUserCommentActivityList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: Comment对象列表

### 2.70 获取用户点赞列表
- **接口**: `/Activity/getUserLike`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.71 获取用户BUG点赞列表
- **接口**: `/Activity/getUserLikeBug`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.72 获取用户建议点赞列表
- **接口**: `/Activity/getUserLikeSuggest`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.73 获取用户动态点赞列表
- **接口**: `/Activity/getUserLikeMoment`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.74 获取用户收藏列表
- **接口**: `/Activity/getUserCollection`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.75 获取用户评论点赞列表
- **接口**: `/Activity/getUserComnnentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.76 获取用户评价点赞列表
- **接口**: `/Activity/getUserEvaluateLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.77 获取用户BUG评论点赞列表
- **接口**: `/Activity/getUserBugComnnentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.78 获取用户建议评论点赞列表
- **接口**: `/Activity/getUserSuggestComnnentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.79 获取用户动态评论点赞列表
- **接口**: `/Activity/getUserMomentCommentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.80 获取用户好价评论点赞列表
- **接口**: `/Activity/getUserGoodPriceComnnentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.81 获取用户BUG、建议和动态评论点赞列表
- **接口**: `/Activity/getUserBugAndSuggestAndMomentComnnentLike`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 2.82 获取加入活动列表
- **接口**: `/Activity/getJoinActivityFinishListByUserCount5`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
- **输出**: Activity对象列表

### 2.83 获取收藏活动列表
- **接口**: `/Activity/getCollectionActivityListByUser`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: Activity对象列表

### 2.84 获取用户评论列表
- **接口**: `/Activity/getUserCommentList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: Comment对象列表

### 2.85 获取用户评价列表
- **接口**: `/Activity/getUserEvaluateList`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: EvaluateActivity对象列表

## 3. Group Purchase模块 (团购相关)

### 3.1 创建团购订单
- **接口**: `/grouppurchase/createGPOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - touid: 目标用户ID
- **输出**: 订单ID

### 3.2 商品收藏
- **接口**: `/grouppurchase/updateProductCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - productid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.3 获取用户收藏的商品
- **接口**: `/grouppurchase/getUserGoodPriceCollectionInfo`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: GoodPiceModel对象列表

### 3.4 取消商品收藏
- **接口**: `/grouppurchase/delProductCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - productid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.5 发布商品评论
- **接口**: `/grouppurchase/updatecomment`
- **方法**: POST
- **输入参数**:
  - commentid: 评论ID（回复时使用）
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 评论内容
  - captchaVerification: 验证码验证信息
- **输出**: 评论ID

### 3.6 删除商品评论
- **接口**: `/grouppurchase/delcomment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - replyid: 回复ID（删除回复时使用）
  - goodpriceid: 商品ID
- **输出**: 操作结果（布尔值）

### 3.7 商品评论点赞
- **接口**: `/grouppurchase/updateCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - goodpriceid: 商品ID
- **输出**: 操作结果（布尔值）

### 3.8 获取商品评论列表
- **接口**: `/grouppurchase/getcomment`
- **方法**: GET
- **输入参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: Comment对象列表

### 3.9 商品点赞
- **接口**: `/grouppurchase/updateGoodPriceLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.10 商品取消点赞
- **接口**: `/grouppurchase/updateCancelLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.11 搜索商品
- **接口**: `/grouppurchase/searchProduct`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
  - ordertype: 排序类型
  - citycode: 城市代码
  - currentIndex: 当前索引
  - isAllCity: 是否所有城市
- **输出**: GoodPiceModel对象列表

### 3.12 获取商品详情
- **接口**: `/grouppurchase/getGoodPriceInfo`
- **方法**: GET
- **输入参数**:
  - goodpriceid: 商品ID
- **输出**: GoodPiceModel对象

### 3.13 提交推荐商品
- **接口**: `/grouppurchase/createGoodPrice`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - title: 标题
  - content: 内容
  - productnum: 商品数量
  - category: 分类
  - brand: 品牌
  - totalprice: 总价
  - price: 价格
  - originalprice: 原价
  - endtime: 结束时间
  - imgs: 图片列表
  - pic: 图片
  - province, city: 省市信息
  - producturl: 商品链接
  - purchasechannels: 购买渠道
  - discount: 折扣
  - lat, lng: 经纬度
  - address, addresstitle: 地址信息
  - captchaVerification: 验证码验证信息
- **输出**: 商品ID

### 3.14 获取热门搜索商品
- **接口**: `/grouppurchase/hotsearchProduct`
- **方法**: GET
- **输入参数**: 无
- **输出**: SearchResult对象列表

### 3.15 获取推荐搜索商品关键词
- **接口**: `/grouppurchase/getRecommendSearchProduct`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
- **输出**: SearchResult对象列表

### 3.16 收藏好价优惠
- **接口**: `/grouppurchase/updateGoodPriceCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.17 获取用户收藏的好价信息
- **接口**: `/grouppurchase/getUserGoodPriceCollectionInfo`
- **方法**: GET
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: GoodPiceModel对象列表

### 3.18 取消好价收藏
- **接口**: `/grouppurchase/delGoodPriceCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.19 商品点不赞
- **接口**: `/grouppurchase/updateUnLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.20 取消商品点不赞
- **接口**: `/grouppurchase/updateCancelUnLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - goodpriceid: 商品ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.21 参加团购活动
- **接口**: `/Activity/joinActivity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - actid: 活动ID
  - uid: 用户ID
  - username: 用户名
  - sex: 性别
- **输出**: Activity对象

### 3.22 客户端支付成功通知
- **接口**: `/Activity/clientPaySuccess`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - orderid: 订单ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.23 获取相关活动列表
- **接口**: `/grouppurchase/getActivityList`
- **方法**: GET
- **输入参数**:
  - goodpriceid: 商品ID
- **输出**: Activity对象列表

### 3.24 更新商品状态
- **接口**: `/grouppurchase/updategoodpricestatus`
- **方法**: POST
- **输入参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
  - token: 用户认证令牌
  - status: 状态
  - msg: 消息
  - tag: 标签
- **输出**: 操作结果（布尔值）

### 3.25 修改推荐商品
- **接口**: `/grouppurchase/updateGoodPrice`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - title: 标题
  - content: 内容
  - productnum: 商品数量
  - category: 分类
  - brand: 品牌
  - totalprice: 总价
  - price: 价格
  - originalprice: 原价
  - endtime: 结束时间
  - imgs: 图片列表
  - pic: 图片
  - province, city: 省市信息
  - producturl: 商品链接
  - purchasechannels: 购买渠道
  - discount: 折扣
  - lat, lng: 经纬度
  - address, addresstitle: 地址信息
  - goodpriceid: 商品ID
- **输出**: 商品ID

### 3.26 获取系统待审核商品列表
- **接口**: `/grouppurchase/getSysGoodPriceCheck`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: GoodPiceModel对象列表

### 3.27 获取我的待审核商品列表
- **接口**: `/grouppurchase/getMyGoodPricePendingList`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: GoodPiceModel对象列表

### 3.28 获取我的已审核商品列表
- **接口**: `/grouppurchase/getMyGoodPriceFinishList`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: GoodPiceModel对象列表

### 3.29 删除我的推荐商品
- **接口**: `/grouppurchase/delMyGoodPrice`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - goodpriceid: 商品ID
- **输出**: 操作结果（布尔值）

### 3.30 获取推荐商品列表
- **接口**: `/grouppurchase/getRecommendGoodPriceList`
- **方法**: GET
- **输入参数**:
  - type: 类型
  - currentIndex: 当前索引
  - citycode: 城市代码
- **输出**: GoodPiceModel对象列表

### 3.31 获取商品规格列表
- **接口**: `/grouppurchase/getSkuStockList`
- **方法**: GET
- **输入参数**:
  - goodpriceid: 商品ID
- **输出**: Skuspecs对象列表

### 3.32 获取商品评价列表
- **接口**: `/grouppurchase/getEvaluateGoodPriceList`
- **方法**: POST
- **输入参数**:
  - goodpriceid: 商品ID
  - currentIndex: 当前索引
- **输出**: EvaluateActivity对象列表

### 3.33 取消商品评论点赞
- **接口**: `/grouppurchase/delCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - likeuid: 被点赞用户ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 3.34 获取用户好价收藏状态
- **接口**: `/grouppurchase/getUserGoodPriceCollection`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

## 4. User模块 (用户相关)

### 4.1 用户登录
- **接口**: `/login`
- **方法**: POST
- **输入参数**:
  - mobile: 手机号
  - email: 邮箱
  - password: 密码
- **输出**: User对象

### 4.2 通过手机号发送验证码
- **接口**: `/user/sendMobileOTP`
- **方法**: GET
- **输入参数**:
  - mobile: 手机号
- **输出**: 操作结果（布尔值）

### 4.3 通过email发送验证码
- **接口**: `/email-code-login`
- **方法**: POST
- **输入参数**:
  - email: 邮箱
- **输出**: 验证令牌

### 4.4 通过uid发送验证码
- **接口**: `/user/sendVCodeByUid`
- **方法**: GET
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 4.5 手机验证登录
- **接口**: `/user/loginmobile`
- **方法**: POST
- **输入参数**:
  - mobile: 手机号
  - vcode: 验证码
  - country: 国家代码
- **输出**: User对象

### 4.6 邮箱登录
- **接口**: `/email-code-login/validity`
- **方法**: POST
- **输入参数**:
  - email: 邮箱
  - code: 验证码
  - token: 验证令牌
- **输出**: User对象

### 4.7 微信登录
- **接口**: `/user/loginweixin`
- **方法**: POST
- **输入参数**:
  - code: 微信授权码
- **输出**: User对象

### 4.8 iOS登录
- **接口**: `/user/loginios`
- **方法**: POST
- **输入参数**:
  - identityToken: 身份令牌
  - iosuserid: iOS用户ID
- **输出**: User对象

### 4.9 支付宝登录注册
- **接口**: `/AliPay/loginali`
- **方法**: POST
- **输入参数**:
  - auth_code: 授权码
- **输出**: User对象

### 4.10 绑定支付宝账号
- **接口**: `/AliPay/updateali`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - auth_code: 授权码
  - confirm: 确认标志
- **输出**: User对象

### 4.11 绑定微信账号
- **接口**: `/user/updateweixin`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - code: 微信授权码
  - confirm: 确认标志
- **输出**: User对象

### 4.12 绑定iOS账号
- **接口**: `/user/updateios`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - identityToken: 身份令牌
  - confirm: 确认标志
  - iosuserid: iOS用户ID
- **输出**: User对象

### 4.13 获取支付宝用户授权请求
- **接口**: `/AliPay/userauth`
- **方法**: POST
- **输入参数**: 无
- **输出**: 授权URL

### 4.14 上传设备信息
- **接口**: `/user/updatePushToken`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - brand: 设备品牌
  - pushtoken: 推送令牌
- **输出**: 操作结果（布尔值）

### 4.15 手机验证码验证
- **接口**: `/user/verifyVCode`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - vcode: 验证码
- **输出**: 操作结果（布尔值）

### 4.16 更新手机号
- **接口**: `/user/updateMobile`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - vcode: 验证码
  - mobile: 手机号
  - country: 国家代码
  - confirm: 确认标志
- **输出**: User对象

### 4.17 用户退出
- **接口**: `/user/userexit`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 操作结果（布尔值）

### 4.18 获取用户信息
- **接口**: `/account/profile`
- **方法**: GET
- **输入参数**:
  - _token: 用户认证令牌
- **输出**: User对象

### 4.19 更新头像（文件上传）
- **接口**: `/user/updateImage`
- **方法**: POST
- **输入参数**:
  - imagefile: 头像文件
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 4.20 更新头像（URL）
- **接口**: `/account/avatar`
- **方法**: POST
- **输入参数**:
  - avatar: 头像URL
- **输出**: 操作结果（布尔值）

### 4.21 更新性别
- **接口**: `/user/updateSex`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - sex: 性别
- **输出**: 操作结果（布尔值）

### 4.22 关注话题
- **接口**: `/user/updateSubject`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - subject: 话题
- **输出**: 操作结果（布尔值）

### 4.23 更新生日
- **接口**: `/user/updateBirthday`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - birthday: 生日
- **输出**: 操作结果（布尔值）

### 4.24 更新昵称
- **接口**: `/account/name`
- **方法**: POST
- **输入参数**:
  - name: 昵称
- **输出**: 操作结果（布尔值）

### 4.25 更新位置
- **接口**: `/user/updateLocation`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - province: 省份
  - city: 城市
- **输出**: 操作结果（布尔值）

### 4.26 更新个人简介
- **接口**: `/user/updateSignature`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - signature: 个人简介
- **输出**: 操作结果（布尔值）

### 4.27 更新密码
- **接口**: `/account/password`
- **方法**: POST
- **输入参数**:
  - _token: 用户认证令牌
  - uid: 用户ID
  - new_password: 新密码（MD5加密）
  - repeat_new_password: 确认新密码（MD5加密）
- **输出**: 操作结果（布尔值）

### 4.28 更新兴趣
- **接口**: `/user/updateInterest`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - interest: 兴趣
- **输出**: 操作结果（布尔值）

### 4.29 更新录音
- **接口**: `/user/updateVoice`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - voice: 录音
- **输出**: 操作结果（布尔值）

### 4.30 用户注销
- **接口**: `/user/deltoken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 4.31 更新活动不感兴趣用户
- **接口**: `/user/updateNotinteresteduids`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - notinteresteduids: 不感兴趣的用户ID
- **输出**: 操作结果（布尔值）

### 4.32 更新好价不感兴趣用户
- **接口**: `/user/goodpricenotinteresteduids`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - goodpricenotinteresteduids: 不感兴趣的好价用户ID
- **输出**: 操作结果（布尔值）

### 4.33 更新黑名单
- **接口**: `/user/updateBlacklist`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - blacklist: 黑名单用户ID
- **输出**: 操作结果（布尔值）

### 4.34 获取关注列表
- **接口**: `/user/getFollow`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
- **输出**: 用户ID列表

### 4.35 检查是否被关注
- **接口**: `/user/selFollwerUser`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - followed: 被关注用户ID
- **输出**: 关注时间

### 4.36 关注用户或社团
- **接口**: `/user/follwerCommunity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - followed: 被关注用户或社团ID
- **输出**: 操作结果（布尔值）

### 4.37 取消关注用户或社团
- **接口**: `/user/cleanfollwerCommunity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - followed: 被取消关注用户或社团ID
- **输出**: 操作结果（布尔值）

### 4.38 获取关注的社团
- **接口**: `/user/getFollowUsers`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: User对象列表

### 4.39 获取关注的社团（首页展示）
- **接口**: `/user/getFollowUsersInCommunityALL`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: User对象列表

### 4.40 获取关注的用户和社团
- **接口**: `/user/getFollowUsersCommunity`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: User对象列表

### 4.41 获取用户粉丝
- **接口**: `/user/getFansUsers`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - currentIndex: 当前索引
- **输出**: User对象列表

### 4.42 获取个人动态
- **接口**: `/user/selUserDynamic`
- **方法**: POST
- **输入参数**:
  - currentIndex: 当前索引
  - uid: 用户ID
- **输出**: Dynamic对象列表

### 4.43 获取私聊关系
- **接口**: `/user/getSingleConversation`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - touid: 目标用户ID
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: GroupRelation对象

### 4.44 创建私聊关系
- **接口**: `/user/joinSingle`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - touid: 目标用户ID
  - uid: 用户ID
  - timeline_id: 时间线ID
  - captchaVerification: 验证码验证信息
  - isCustomer: 是否为客服（0或1）
- **输出**: GroupRelation对象

### 4.45 获取其他用户信息
- **接口**: `/user/getuserinfo`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
- **输出**: User对象

### 4.46 发送加好友请求
- **接口**: `/user/updateMemberJoin`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 内容
- **输出**: 操作结果（布尔值）

### 4.47 分享好友
- **接口**: `/user/updateSharedFriend`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - contentid: 内容ID
  - touids: 目标用户IDs
  - sharedtype: 分享类型
  - content: 内容
  - image: 图片
  - fromuid: 来源用户ID
- **输出**: 操作结果（布尔值）

### 4.48 获取我的待付款订单
- **接口**: `/grouppurchase/getMyPendingOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: Order对象列表

### 4.49 获取已完成付款的订单
- **接口**: `/grouppurchase/getMyFinishOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: Order对象列表

### 4.50 获取已退款的订单
- **接口**: `/grouppurchase/getMyRefundOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: Order对象列表

### 4.51 获取已确认的订单
- **接口**: `/grouppurchase/getMyConfirmOrder`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: Order对象列表

## 5. IM模块 (即时通讯相关)

### 5.1 发送群聊消息
- **接口**: `/IM/sendGroupMessage` (活动和团购)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - content: 消息内容
  - contenttype: 内容类型
  - captchaVerification: 验证码验证信息
- **输出**: 消息ID

### 5.2 发送社团消息
- **接口**: `/IM/sendCommunityMessage`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - content: 消息内容
  - contenttype: 内容类型
  - captchaVerification: 验证码验证信息
- **输出**: 消息ID

### 5.3 发送私聊消息
- **接口**: `/IM/sendSingleMessage`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - content: 消息内容
  - contenttype: 内容类型
  - captchaVerification: 验证码验证信息
- **输出**: 消息ID

### 5.4 获取群聊成员
- **接口**: `/IM/getGroupAllUsers`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: User对象列表

### 5.5 撤回消息
- **接口**: `/IM/recallMessage`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - username: 用户名
  - source_id: 源消息ID
  - relationtype: 关系类型
- **输出**: 操作结果（布尔值）

### 5.6 聊天中拉黑用户
- **接口**: `/IM/updateBlockUser` (私聊)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.7 聊天中拉黑用户
- **接口**: `/IM/updateBlockActivity` (活动)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.8 聊天中拉黑用户
- **接口**: `/IM/updateBlockCommunity` (社团)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.9 聊天中取消拉黑用户
- **接口**: `/IM/updateCancelBlockUser` (私聊)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.10 聊天中取消拉黑用户
- **接口**: `/IM/updateCancelBlockActivity` (活动)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.11 聊天中取消拉黑用户
- **接口**: `/IM/updateCancelBlockCommunity` (社团)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
- **输出**: 操作结果（布尔值）

### 5.12 举报聊天群
- **接口**: `/IM/reportOtherIm`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - timeline_id: 时间线ID
  - reporttype: 举报类型
  - reportcontent: 举报内容
  - images: 图片
- **输出**: 举报ID

### 5.13 获取我的举报详情
- **接口**: `/IM/getMyImReportInfo`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - reportid: 举报ID
- **输出**: ImReport对象

### 5.14 获取我的举报
- **接口**: `/IM/getMyImReport`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: ImReport对象列表

### 5.15 同步群聊关系
- **接口**: `/IM/listMyGroupConversations`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 5.16 同步活动群聊关系
- **接口**: `/IM/listActivityGroupConversations`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 5.17 同步活动群聊关系初始化
- **接口**: `/IM/listActivityGroupConversationsInit`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 5.18 同步社团群聊关系
- **接口**: `/IM/listCommunityGroupConversations`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 5.19 同步私聊关系
- **接口**: `/IM/listSingleGroupConversations`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: GroupRelation对象列表

### 5.20 已读消息（私聊）
- **接口**: `/IM/postSingleReadMessage`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: 操作结果（布尔值）

### 5.21 已读消息（活动关系）
- **接口**: `/IM/updateGroupMessageAlready`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: 操作结果（布尔值）

### 5.22 已读消息（社团）
- **接口**: `/IM/updateCommunityMessageAlready`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: 操作结果（布尔值）

### 5.23 获取聊天记录
- **接口**: `/IM/getGroupConversationTimelineId` (活动)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: TimeLineSync对象列表

### 5.24 获取聊天记录
- **接口**: `/IM/getCommunityConversationTimelineId` (社团)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: TimeLineSync对象列表

### 5.25 获取聊天记录
- **接口**: `/IM/getSingleConversationTimelineId` (私聊)
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - sequence_id: 序列ID
- **输出**: TimeLineSync对象列表

### 5.26 创建现金红包
- **接口**: `/user/createRedPacketOrder`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - timeline_id: 时间线ID
  - amount: 金额
  - redpackettype: 红包类型
  - redpacketnum: 红包数量
  - content: 内容
  - timeline_type: 时间线类型
- **输出**: 订单信息

### 5.27 验证红包是否成功
- **接口**: `/AliPay/payredpacketsuccess`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - result: 结果
  - sign: 签名
- **输出**: 红包ID

### 5.28 获取红包详情
- **接口**: `/IM/getUserRedPacketByRedpacketid`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - redpacketid: 红包ID
- **输出**: RedPacketModel对象

### 5.29 领取红包
- **接口**: `/IM/receiveRedPacket`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - redpacketid: 红包ID
- **输出**: 领取金额

### 5.30 获取红包领用情况
- **接口**: `/IM/getRedPacketDetailList`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - redpacketid: 红包ID
- **输出**: RedPacketDetail对象列表

### 5.31 举报BUG
- **接口**: `/IM/reportBUG`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - reportcontent: 举报内容
  - images: 图片
  - captchaVerification: 验证码验证信息
- **输出**: 举报ID

### 5.32 举报建议
- **接口**: `/IM/reportSuggest`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - reportcontent: 举报内容
  - images: 图片
  - captchaVerification: 验证码验证信息
- **输出**: 举报ID

### 5.33 发布动态
- **接口**: `/IM/reportMoment`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - content: 内容
  - voice: 音频
  - images: 图片
  - coverimgwh: 封面图宽高比
  - category: 分类
  - captchaVerification: 验证码验证信息
- **输出**: 动态ID

### 5.34 删除动态
- **接口**: `/IM/delMoment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - momentid: 动态ID
- **输出**: 操作结果（布尔值）

### 5.35 获取BUG列表
- **接口**: `/IM/getBugList`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - currIndex: 当前索引
- **输出**: Bug对象列表

### 5.36 获取BUG详情
- **接口**: `/IM/getBugInfo`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - bugid: BUG ID
- **输出**: Bug对象

### 5.37 获取建议列表
- **接口**: `/IM/getSuggestList`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - currIndex: 当前索引
- **输出**: Suggest对象列表

### 5.38 获取建议详情
- **接口**: `/IM/getSuggestInfo`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
  - token: 用户认证令牌
  - suggestid: 建议ID
- **输出**: Suggest对象

### 5.39 获取动态列表
- **接口**: `/IM/getMomentList`
- **方法**: POST
- **输入参数**:
  - currIndex: 当前索引
  - subject: 主题
- **输出**: Moment对象列表

### 5.40 获取动态详情
- **接口**: `/IM/getMomentInfo`
- **方法**: POST
- **输入参数**:
  - momentid: 动态ID
- **输出**: Moment对象

### 5.41 获取用户动态列表
- **接口**: `/IM/getMomentListByUser`
- **方法**: POST
- **输入参数**:
  - uid: 用户ID
- **输出**: Moment对象列表

### 5.42 BUG点赞
- **接口**: `/IM/updateBugLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - bugid: BUG ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.43 取消BUG点赞
- **接口**: `/IM/delBugLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - bugid: BUG ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.44 建议点赞
- **接口**: `/IM/updateSuggestLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - suggestid: 建议ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.45 取消建议点赞
- **接口**: `/IM/delSuggestLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - suggestid: 建议ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.46 动态点赞
- **接口**: `/IM/updateMomentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - momentid: 动态ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.47 取消动态点赞
- **接口**: `/IM/delMomentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - momentid: 动态ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.48 发布BUG评论
- **接口**: `/IM/updateBugComment`
- **方法**: POST
- **输入参数**:
  - commentid: 评论ID（回复时使用）
  - token: 用户认证令牌
  - bugid: BUG ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 评论内容
  - captchaVerification: 验证码验证信息
- **输出**: 评论ID

### 5.49 发布建议评论
- **接口**: `/IM/updateSuggestComment`
- **方法**: POST
- **输入参数**:
  - commentid: 评论ID（回复时使用）
  - token: 用户认证令牌
  - suggestid: 建议ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 评论内容
  - captchaVerification: 验证码验证信息
- **输出**: 评论ID

### 5.50 发布动态评论
- **接口**: `/IM/updateMomentComment`
- **方法**: POST
- **输入参数**:
  - commentid: 评论ID（回复时使用）
  - token: 用户认证令牌
  - momentid: 动态ID
  - uid: 用户ID
  - touid: 目标用户ID
  - content: 评论内容
  - captchaVerification: 验证码验证信息
- **输出**: 评论ID

### 5.51 删除BUG评论
- **接口**: `/IM/delBugComment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - replyid: 回复ID
  - bugid: BUG ID
- **输出**: 操作结果（布尔值）

### 5.52 删除建议评论
- **接口**: `/IM/delSuggestComment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - replyid: 回复ID
  - suggestid: 建议ID
- **输出**: 操作结果（布尔值）

### 5.53 删除动态评论
- **接口**: `/IM/delMomentComment`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - replyid: 回复ID
  - momentid: 动态ID
- **输出**: 操作结果（布尔值）

### 5.54 获取BUG评论列表
- **接口**: `/IM/getBugComment`
- **方法**: GET
- **输入参数**:
  - bugid: BUG ID
  - uid: 用户ID
- **输出**: Comment对象列表

### 5.55 获取建议评论列表
- **接口**: `/IM/getSuggestComment`
- **方法**: GET
- **输入参数**:
  - suggestid: 建议ID
  - uid: 用户ID
- **输出**: Comment对象列表

### 5.56 获取动态评论列表
- **接口**: `/IM/getMomentComment`
- **方法**: GET
- **输入参数**:
  - momentid: 动态ID
- **输出**: Comment对象列表

### 5.57 BUG评论点赞
- **接口**: `/IM/updateBugCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - bugid: BUG ID
- **输出**: 操作结果（布尔值）

### 5.58 取消BUG评论点赞
- **接口**: `/IM/delBugCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - likeuid: 被点赞用户ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.59 建议评论点赞
- **接口**: `/IM/updateSuggestCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - suggestid: 建议ID
- **输出**: 操作结果（布尔值）

### 5.60 取消建议评论点赞
- **接口**: `/IM/delSuggestCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - likeuid: 被点赞用户ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.61 动态评论点赞
- **接口**: `/IM/updateMomentCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - uid: 用户ID
  - likeuid: 被点赞用户ID
  - momentid: 动态ID
- **输出**: 操作结果（布尔值）

### 5.62 取消动态评论点赞
- **接口**: `/IM/delMomentCommentLike`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - commentid: 评论ID
  - likeuid: 被点赞用户ID
  - uid: 用户ID
- **输出**: 操作结果（布尔值）

### 5.63 创建社团
- **接口**: `/Community/createCommunity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - communityname: 社团名称
  - province: 省份
  - city: 城市
  - clubicon: 社团图标
  - notice: 公告
  - joinrule: 加入规则
  - members: 成员列表
  - membernames: 成员名称列表
- **输出**: Community对象

### 5.64 更新社团图片
- **接口**: `/Community/updateCommunityPicture`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - cid: 社团ID
  - path: 图片路径
- **输出**: 操作结果（布尔值）

### 5.65 获取社团成员列表
- **接口**: `/Community/getCommunityMember`
- **方法**: POST
- **输入参数**:
  - cid: 社团ID
  - currentIndex: 当前索引
- **输出**: User对象列表

### 5.66 删除社团成员
- **接口**: `/Community/delCommunityMember`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - cid: 社团ID
  - memberid: 成员ID
- **输出**: 操作结果（布尔值）

### 5.67 退出社团
- **接口**: `/Community/delQuiteCommunity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - cid: 社团ID
- **输出**: 操作结果（布尔值）

### 5.68 邀请好友加入社团
- **接口**: `/Community/joinCommunity`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
  - timeline_id: 时间线ID
  - members: 成员列表
  - oldmembers: 原成员
  - membernames: 成员名称列表
- **输出**: 操作结果（布尔值）

### 5.69 搜索动态热门关键词
- **接口**: `/IM/hotsearchMoment`
- **方法**: POST
- **输入参数**: 无
- **输出**: SearchResult对象列表

### 5.70 搜索动态关键词推荐
- **接口**: `/IM/getRecommendSearchMoment`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
- **输出**: SearchResult对象列表

### 5.71 搜索动态
- **接口**: `/IM/searchMoment`
- **方法**: POST
- **输入参数**:
  - content: 搜索内容
  - currentIndex: 当前索引
- **输出**: Moment对象列表

## 6. 阿里云服务模块

### 6.1 获取用户资料安全令牌
- **接口**: `/user/getUserProfileSecurityToken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: SecurityToken对象

### 6.2 获取活动安全令牌
- **接口**: `/Community/getActivitySecurityToken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: SecurityToken对象

### 6.3 获取BUG安全令牌
- **接口**: `/user/getBugSecurityToken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: SecurityToken对象

### 6.4 获取动态安全令牌
- **接口**: `/user/getMomentSecurityToken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: SecurityToken对象

### 6.5 获取语音安全令牌
- **接口**: `/IM/getSoundSecurityToken`
- **方法**: POST
- **输入参数**:
  - token: 用户认证令牌
  - uid: 用户ID
- **输出**: SecurityToken对象

## 7. 系统配置模块

### 7.1 获取活动类型列表
- **接口**: `/Activity/getActivityTypeList`
- **方法**: GET
- **输入参数**: 无
- **输出**: 活动类型列表

### 7.2 根据名称获取活动类型列表
- **接口**: `/Activity/getActivityTypeListByTypeName`
- **方法**: POST
- **输入参数**:
  - typename: 类型名称
- **输出**: 活动类型列表

### 7.3 获取系统配置参数
- **接口**: `/SysConfig/getConfigParameter`
- **方法**: GET
- **输入参数**:
  - parameterkey: 参数键名（如"userimgconfig"、"purchasechannels"、"messagreport"、"syshelp"）
- **输出**: 系统配置参数

### 7.4 获取应用版本信息
- **接口**: `/SysConfig/getAppversion`
- **方法**: GET
- **输入参数**: 无
- **输出**: AppInfo对象

### 7.5 获取系统客服
- **接口**: `/SysConfig/getSysCustomer`
- **方法**: GET
- **输入参数**:
  - categoryid: 分类ID
  - uid: 用户ID
  - token: 用户认证令牌
- **输出**: 客服用户ID

### 7.6 获取文件内容
- **接口**: `/SysConfig/getFileContent`
- **方法**: GET
- **输入参数**:
  - parameterkey: 参数键名（如"phonecode"、"sysNotice"）
- **输出**: 文件内容

## 8. 高德地图服务模块

### 8.1 周边地点搜索
- **接口**: `/v5/place/around` (高德API)
- **方法**: GET
- **输入参数**:
  - key: API密钥
  - location: 经纬度坐标
  - types: POI类型
  - page_size: 每页记录数
  - page_num: 页码
- **输出**: POI搜索结果

### 8.2 文本地点搜索
- **接口**: `/v5/place/text` (高德API)
- **方法**: GET
- **输入参数**:
  - key: API密钥
  - keywords: 搜索关键词
  - types: POI类型
  - region: 区域
  - citylimit: 是否限制城市内搜索
  - page_size: 每页记录数
  - page_num: 页码
- **输出**: POI搜索结果
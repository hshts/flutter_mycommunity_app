# 社区应用缓存表结构文档

## 1. 表概述

该文档详细描述了社区应用中使用的SQLite本地缓存表结构，包括表名、字段名、数据类型和字段描述。这些表用于存储用户数据、消息记录、点赞状态、收藏状态等，以提升应用性能和用户体验。

## 2. 表结构详情

### 2.1 im_group_relation_table (IM群组关系表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | INTEGER | ID |
| timeline_id | TEXT | 时间线ID |
| readindex | INTEGER | 已读索引 |
| unreadcount | INTEGER | 未读数量 |
| group_name1 | TEXT | 群组名称 |
| clubicon | TEXT | 社团图标 |
| name | TEXT | 名称 |
| newmsgtime | TEXT | 新消息时间 |
| newmsg | TEXT | 新消息内容 |
| timelineType | INTEGER | 时间线类型 |
| uid | INTEGER | 用户ID |
| istop | INTEGER | 是否置顶 |
| isdel | INTEGER | 是否删除 |
| relationtype | INTEGER | 关系类型 |
| status | INTEGER | 状态 |
| locked | INTEGER | 是否锁定 |
| memberupdatetime | TEXT | 成员更新时间 |
| oldmemberupdatetime | TEXT | 旧成员更新时间 |
| isnotservice | INTEGER | 是否非服务 |
| source_id | TEXT | 源ID |
| goodpriceid | TEXT | 商品ID |

### 2.2 Comment_Reply_table (评论回复表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| replyid | INTEGER | 回复ID |
| actid | TEXT | 活动ID |
| commentid | INTEGER | 评论ID |
| replycontent | TEXT | 回复内容 |
| uid | INTEGER | 用户ID |
| isread | INTEGER | 是否已读 |
| replycreatetime | TEXT | 回复创建时间 |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| touid | INTEGER | 目标用户ID |
| type | TEXT | 类型 |
| ismaster | INTEGER | 是否楼主 |
| actcontent | TEXT | 活动内容 |
| coverimg | TEXT | 封面图片 |
| evaluateid | INTEGER | 评价ID |
| imagepaths | TEXT | 图片路径 |

### 2.3 user_config (用户配置表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| nopromptActRule | INTEGER | 不再提示活动规则 |

### 2.4 t_like (点赞表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| likeid | INTEGER | 点赞ID |
| touid | INTEGER | 目标用户ID |
| liketype | INTEGER | 点赞类型 |
| contentid | TEXT | 内容ID |
| uid | INTEGER | 用户ID |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| isread | INTEGER | 是否已读 |
| createtime | TEXT | 创建时间 |

### 2.5 user_notinteresteduids (用户不感兴趣UID表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| notinteresteduid | INTEGER | 不感兴趣的用户ID |

### 2.6 user_goodnotinteresteduids (用户不感兴趣商品UID表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| goodpricenotinteresteduid | INTEGER | 不感兴趣的商品用户ID |

### 2.7 user_blacklist (用户黑名单表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| blacklistuid | INTEGER | 黑名单用户ID |

### 2.8 sys_config (系统配置表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| sysname | TEXT | 系统名称 |
| content | TEXT | 内容 |

### 2.9 t_Follow (关注表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| profilepicture | TEXT | 用户头像 |
| username | TEXT | 用户名 |
| isread | INTEGER | 是否已读 |
| fans | INTERGER | 粉丝 |
| createtime | TEXT | 创建时间 |
| id | INTEGER | ID |
| type | INTERGER | 类型 |

### 2.10 user_member_state_table (用户成员状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | INTEGER | ID |
| uid | INTEGER | 用户ID |
| touid | INTEGER | 目标用户ID |
| content | TEXT | 内容 |
| createtime | TEXT | 创建时间 |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| status | INTEGER | 状态 |
| isread | INTEGER | 是否已读 |

### 2.11 im_groupandcommunity_member_relation (群组和社团成员关系表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| timeline_id | TEXT | 时间线ID |
| uid | INTEGER | 用户ID |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |

### 2.12 user_friend_state_table (用户朋友状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | INTEGER | ID |
| uid | INTEGER | 用户ID |
| touid | INTEGER | 目标用户ID |
| createtime | TEXT | 创建时间 |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| status | INTEGER | 状态 |
| isread | INTEGER | 是否已读 |

### 2.13 user_shared_state_table (用户分享状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| sharedid | INTEGER | 分享ID |
| uid | INTEGER | 用户ID |
| fromuid | INTEGER | 来源用户ID |
| contentid | TEXT | 内容ID |
| content | TEXT | 内容 |
| image | TEXT | 图片 |
| sharedtype | INTEGER | 分享类型 |
| createtime | TEXT | 创建时间 |
| fromusername | TEXT | 来源用户名 |
| fromprofilepicture | TEXT | 来源用户头像 |
| mincost | REAL | 最小费用 |
| maxcost | REAL | 最大费用 |
| lat | REAL | 纬度 |
| lng | REAL | 经度 |
| isread | INTEGER | 是否已读 |

### 2.14 user_order_state_table (用户订单状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| ordertype | INTEGER | 订单类型 |
| ordercount | INTEGER | 订单数量 |

### 2.15 user_orderunevaluate_state_table (用户未评价订单状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| orderunevaluatecount | INTEGER | 未评价订单数量 |

### 2.16 im_user_relation_table (IM用户关系表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| id | INTEGER | ID |
| timeline_id | TEXT | 时间线ID |
| readindex | INTEGER | 已读索引 |
| unreadcount | INTEGER | 未读数量 |
| group_name1 | TEXT | 群组名称 |
| clubicon | TEXT | 社团图标 |
| name | TEXT | 名称 |
| newmsgtime | TEXT | 新消息时间 |
| newmsg | TEXT | 新消息内容 |
| timelineType | INTEGER | 时间线类型 |
| uid | INTEGER | 用户ID |

### 2.17 activity_state_table (活动状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actid | TEXT | 活动ID |
| uid | INTEGER | 用户ID |

### 2.18 bugsuggest_state_table (BUG建议状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actid | TEXT | 活动ID |
| uid | INTEGER | 用户ID |
| type | INTEGER | 类型 |

### 2.19 goodprice_state_table (商品价格状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| goodpriceid | TEXT | 商品价格ID |
| uid | INTEGER | 用户ID |
| status | INTEGER | 状态 |

### 2.20 activity_collection_state_table (活动收藏状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actid | TEXT | 活动ID |
| peoplenum | INTEGER | 人数 |
| femalenum | INTEGER | 女性人数 |
| malenum | INTEGER | 男性人数 |
| content | TEXT | 内容 |
| coverimg | TEXT | 封面图片 |
| uid | INTEGER | 用户ID |
| actsex | TEXT | 活动性别要求 |
| actprovince | TEXT | 活动省份 |
| actcity | TEXT | 活动城市 |
| coverimgwh | TEXT | 封面图片宽高比 |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| lat | REAL | 纬度 |
| lng | REAL | 经度 |
| cost | REAL | 费用 |
| localuid | INTEGER | 本地用户ID |
| maxcost | REAL | 最大费用 |
| mincost | REAL | 最小费用 |

### 2.21 product_collection_state_table (商品收藏状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| productid | INTEGER | 商品ID |
| uid | INTEGER | 用户ID |

### 2.22 goodprice_collection_state_table (商品价格收藏状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| goodpriceid | TEXT | 商品价格ID |
| title | TEXT | 标题 |
| content | TEXT | 内容 |
| productnum | INTEGER | 商品数量 |
| category | INTEGER | 分类 |
| brand | TEXT | 品牌 |
| totalprice | REAL | 总价 |
| price | REAL | 价格 |
| originalprice | REAL | 原价 |
| discount | REAL | 折扣 |
| endtime | TEXT | 结束时间 |
| createtime | TEXT | 创建时间 |
| albumpics | TEXT | 相册图片 |
| pic | TEXT | 图片 |
| collectionnum | INTEGER | 收藏数量 |
| province | TEXT | 省份 |
| city | TEXT | 城市 |
| uid | INTEGER | 用户ID |
| producturl | TEXT | 商品链接 |
| likenum | INTEGER | 点赞数 |
| unlikenum | INTEGER | 不喜欢数 |
| purchasechannels | TEXT | 购买渠道 |
| productstatus | INTEGER | 商品状态 |
| satisfactionrate | REAL | 满意度 |
| activitycount | INTEGER | 活动数 |
| lat | REAL | 纬度 |
| lng | REAL | 经度 |
| address | TEXT | 地址 |
| addresstitle | TEXT | 地址标题 |
| commentnum | INTEGER | 评论数 |
| tag | TEXT | 标签 |
| username | TEXT | 用户名 |
| profilepicture | TEXT | 用户头像 |
| localuid | INTEGER | 本地用户ID |
| mincost | REAL | 最小费用 |
| maxcost | REAL | 最大费用 |

### 2.23 activity_comment_state_table (活动评论状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| commentid | TEXT | 评论ID |
| uid | INTEGER | 用户ID |

### 2.24 goodprice_comment_state_table (商品价格评论状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| commentid | TEXT | 评论ID |
| uid | INTEGER | 用户ID |

### 2.25 activity_bugsuggestcomment_state_table (活动BUG建议评论状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| commentid | TEXT | 评论ID |
| uid | INTEGER | 用户ID |
| type | INTEGER | 类型 |

### 2.26 activity_evaluate_state_table (活动评价状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| evaluateid | TEXT | 评价ID |
| uid | INTEGER | 用户ID |

### 2.27 community_follow_state_table (社团关注状态表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| uid | INTEGER | 用户ID |
| follow | INTEGER | 关注 |

### 2.28 history_browse_table (历史浏览表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actid | TEXT | 活动ID |
| browsetime | TEXT | 浏览时间 |
| content | TEXT | 内容 |
| uid | INTERGER | 用户ID |
| coverimgwh | TEXT | 封面图片宽高比 |
| coverimg | TEXT | 封面图片 |
| profilepicture | TEXT | 用户头像 |
| username | TEXT | 用户名 |
| actsex | TEXT | 活动性别要求 |
| femalenum | INTERGER | 女性人数 |
| malenum | INTERGER | 男性人数 |
| peoplenum | INTERGER | 人数 |
| mincost | REAL | 最小费用 |
| maxcost | REAL | 最大费用 |

### 2.29 history_search_table (历史搜索表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| content | TEXT | 内容 |
| time | TEXT | 时间 |
| type | INTEGER | 类型 |
| uid | INTEGER | 用户ID |

### 2.30 unevaluate_activity (未评价活动表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| actevaluateid | INTEGER | 活动评价ID |
| actid | TEXT | 活动ID |
| createtime | TEXT | 创建时间 |
| content | TEXT | 内容 |
| uid | INTERGER | 用户ID |
| coverimgwh | TEXT | 封面图片宽高比 |
| coverimg | TEXT | 封面图片 |
| profilepicture | TEXT | 用户头像 |
| username | TEXT | 用户名 |
| femalenum | INTERGER | 女性人数 |
| malenum | INTERGER | 男性人数 |
| peoplenum | INTERGER | 人数 |
| evaluatestatus | INTEGER | 评价状态 |
| currentpeoplenum | INTERGER | 当前人数 |
| actuid | INTEGER | 活动用户ID |

### 2.31 im_timeline_sync_relation (IM时间线同步关系表)

| 字段名 | 数据类型 | 描述 |
|--------|---------|------|
| sequence_id | INTEGER | 序列ID |
| timeline_id | TEXT | 时间线ID |
| conversation | INTEGER | 会话 |
| send_time | TEXT | 发送时间 |
| sender | INTEGER | 发送者 |
| serdername | TEXT | 发送者名称 |
| serderpicture | TEXT | 发送者头像 |
| content | TEXT | 内容 |
| contenttype | INTEGER | 内容类型 |
| uid | INTEGER | 用户ID |
| localpath | TEXT | 本地路径 |
| isopen | INTEGER | 是否打开 |
| source_id | TEXT | 源ID |
# API 文档：根据城市获取活动列表

## 接口信息

- **接口名称**: 根据城市获取活动列表
- **接口路径**: `/Activity/getActivityListByCity`
- **请求方法**: `GET`
- **接口编号**: 2.25

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| citycode | string | 是 | - | 城市代码（如：440300表示深圳） |
| currentIndex | integer | 否 | 0 | 分页起始索引 |
| pageSize | integer | 否 | 20 | 每页返回数量（最大100） |
| orderBy | string | 否 | updatetime | 排序字段，可选值：<br>- updatetime: 按更新时间<br>- createtime: 按创建时间<br>- likenum: 按点赞数<br>- viewnum: 按浏览数 |

## 请求示例

### 基本请求
```http
GET /Activity/getActivityListByCity?citycode=440300
```

### 带分页和排序的请求
```http
GET /Activity/getActivityListByCity?citycode=440300&currentIndex=0&pageSize=20&orderBy=likenum
```

## 响应数据

### 成功响应 (200)

```json
{
  "data": [
    {
      "actid": "act_1234567890abcdef",
      "content": "深圳周末户外徒步活动",
      "createtime": "2025-10-15T10:30:00",
      "updatetime": "2025-10-15T12:00:00",
      "status": 1,
      "peoplenum": 20,
      "currentpeoplenum": 15,
      "startyear": 1729065600,
      "endyear": 1729152000,
      "address": "深圳市南山区梧桐山",
      "addresstitle": "梧桐山风景区",
      "lat": 22.5963,
      "lng": 114.1901,
      "actcity": "440300",
      "actprovince": "440000",
      "coverimg": "https://example.com/images/cover1.jpg",
      "coverimgwh": "800x600",
      "actimagespath": "img1.jpg,img2.jpg,img3.jpg",
      "maxcost": 100.0,
      "mincost": 50.0,
      "paytype": 1,
      "uid": 1001,
      "goodpriceid": "gp_123456",
      "likenum": 125,
      "collectionnum": 68,
      "commentnum": 42,
      "viewnum": 2580,
      "joinnum": 15,
      "locked": 0
    }
  ],
  "citycode": "440300",
  "currentIndex": 0,
  "pageSize": 20,
  "count": 1
}
```

### 错误响应

#### 缺少必填参数 (400)
```json
{
  "error": "Missing citycode parameter"
}
```

#### 参数格式错误 (400)
```json
{
  "error": "Invalid parameter format"
}
```

#### 服务器错误 (500)
```json
{
  "error": "Internal server error message"
}
```

## 字段说明

### Activity 对象字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| actid | string | 活动唯一标识 |
| content | string | 活动内容描述 |
| createtime | string | 创建时间（ISO 8601格式） |
| updatetime | string | 更新时间（ISO 8601格式） |
| status | integer | 活动状态：1=进行中, 2=已结束 |
| peoplenum | integer | 活动总人数限制 |
| currentpeoplenum | integer | 当前参与人数 |
| startyear | integer | 开始时间戳（Unix时间戳） |
| endyear | integer | 结束时间戳（Unix时间戳） |
| address | string | 活动详细地址 |
| addresstitle | string | 地址标题/名称 |
| lat | float | 纬度 |
| lng | float | 经度 |
| actcity | string | 活动所在城市代码 |
| actprovince | string | 活动所在省份代码 |
| coverimg | string | 封面图片URL |
| coverimgwh | string | 封面图片宽高比 |
| actimagespath | string | 活动图片列表（逗号分隔） |
| maxcost | float | 最大费用 |
| mincost | float | 最小费用 |
| paytype | integer | 支付类型：0=免费, 1=后付款, 2=先付款 |
| uid | integer | 发起人用户ID |
| goodpriceid | string | 关联商品ID |
| likenum | integer | 点赞数 |
| collectionnum | integer | 收藏数 |
| commentnum | integer | 评论数 |
| viewnum | integer | 浏览数 |
| joinnum | integer | 参与数 |
| locked | integer | 是否锁定（活动开始后） |

## 业务逻辑

1. **城市过滤**: 根据提供的 citycode 筛选活动
2. **排序规则**: 
   - 默认按更新时间降序
   - 可选按创建时间、点赞数、浏览数排序
   - 所有排序都是降序
3. **分页**: 使用 currentIndex 和 pageSize 进行分页
4. **返回值**: 包含活动列表和分页信息

## 使用场景

- 在城市活动页面展示本地活动
- 按不同维度（热度、时间）浏览活动
- 实现无限滚动加载

## 注意事项

1. citycode 必须提供，否则返回 400 错误
2. 排序字段如果不在允许列表中，会自动使用默认值 updatetime
3. pageSize 建议不超过 100，以保证响应速度
4. 时间字段使用 ISO 8601 格式，便于前端解析

## 相关接口

- `GET /Activity/getActivityListByUpdateTime` - 根据更新时间获取活动（支持城市过滤）
- `GET /Activity/getActivityListByUser` - 根据用户获取活动列表
- `GET /Activity/getActivity` - 获取单个活动详情

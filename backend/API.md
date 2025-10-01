# API接口文档

## 基础信息
- 服务地址: http://localhost:5000
- API前缀: /grouppurchase
- 数据格式: JSON
- 字符编码: UTF-8

## 响应格式
```json
{
    "code": 200,
    "message": "操作成功",
    "success": true,
    "data": {}
}
```

## 团购商品接口

### 1. 获取热门搜索关键词
- **接口**: GET /grouppurchase/hotsearchProduct
- **说明**: 获取热门搜索关键词列表
- **参数**: 无
- **响应示例**:
```json
{
    "code": 200,
    "message": "获取热门搜索成功",
    "success": true,
    "data": [
        {"keyword": "手机", "count": 1000},
        {"keyword": "电脑", "count": 800}
    ]
}
```

### 2. 获取推荐搜索关键词
- **接口**: POST /grouppurchase/getRecommendSearchProduct
- **说明**: 根据输入内容获取推荐搜索关键词
- **参数**:
  - content: 搜索内容
- **响应**: 返回匹配的关键词列表

### 3. 搜索商品
- **接口**: POST /grouppurchase/searchProduct
- **说明**: 搜索商品信息
- **参数**:
  - content: 搜索关键词
  - ordertype: 排序方式 (time/price_asc/price_desc/hot)
  - citycode: 城市代码
  - currentIndex: 页码索引
  - isAllCity: 是否全国 (1/0)

### 4. 获取商品详情
- **接口**: GET /grouppurchase/getGoodPriceInfo
- **说明**: 获取指定商品的详细信息
- **参数**:
  - goodpriceid: 商品ID

### 5. 获取推荐商品列表
- **接口**: GET /grouppurchase/getRecommendGoodPriceList
- **说明**: 获取推荐商品列表
- **参数**:
  - type: 类型 (1-最新, 2-热门, 3-推荐)
  - currentIndex: 页码索引
  - citycode: 城市代码

## 收藏相关接口

### 6. 收藏商品
- **接口**: POST /grouppurchase/updateGoodPriceCollection
- **说明**: 收藏好价商品
- **参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
  - token: 用户令牌
- **认证**: 需要Authorization头部

### 7. 取消收藏
- **接口**: POST /grouppurchase/delGoodPriceCollection
- **说明**: 取消收藏好价商品
- **参数**: 同收藏接口

### 8. 获取用户收藏列表
- **接口**: GET /grouppurchase/getUserGoodPriceCollectionInfo
- **说明**: 获取用户收藏的商品列表
- **参数**:
  - currentIndex: 页码索引
  - uid: 用户ID
  - token: 用户令牌

## 评论相关接口

### 9. 添加评论
- **接口**: POST /grouppurchase/updatecomment
- **说明**: 为商品添加评论或回复
- **参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
  - touid: 被回复用户ID(可选)
  - content: 评论内容
  - commentid: 父评论ID(回复时使用)
  - token: 用户令牌

### 10. 获取评论列表
- **接口**: GET /grouppurchase/getcomment
- **说明**: 获取商品的评论列表
- **参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID

### 11. 删除评论
- **接口**: POST /grouppurchase/delcomment
- **说明**: 删除评论或回复
- **参数**:
  - commentid: 评论ID
  - replyid: 回复ID
  - uid: 用户ID
  - goodpriceid: 商品ID
  - token: 用户令牌

### 12. 点赞评论
- **接口**: POST /grouppurchase/updateCommentLike
- **说明**: 为评论点赞
- **参数**:
  - commentid: 评论ID
  - uid: 用户ID
  - goodpriceid: 商品ID
  - token: 用户令牌

### 13. 取消点赞评论
- **接口**: POST /grouppurchase/delCommentLike
- **说明**: 取消评论点赞
- **参数**:
  - commentid: 评论ID
  - uid: 用户ID
  - token: 用户令牌

## 点赞相关接口

### 14. 商品点赞
- **接口**: POST /grouppurchase/updateGoodPriceLike
- **说明**: 为商品点赞
- **参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
  - token: 用户令牌

### 15. 取消商品点赞
- **接口**: POST /grouppurchase/updateCancelLike
- **说明**: 取消商品点赞
- **参数**: 同点赞接口

## 商品管理接口

### 16. 创建商品
- **接口**: POST /grouppurchase/createGoodPrice
- **说明**: 创建新的好价商品
- **参数**:
  - title: 商品标题
  - content: 商品描述
  - price: 商品价格
  - originalprice: 原价
  - pic: 商品图片
  - category: 商品分类
  - province: 省份
  - city: 城市
  - purchasechannels: 购买渠道
  - producturl: 商品链接
  - uid: 用户ID
  - token: 用户令牌

### 17. 获取我的待审核商品
- **接口**: GET /grouppurchase/getMyGoodPricePendingList
- **说明**: 获取当前用户待审核的商品列表
- **参数**:
  - uid: 用户ID
  - token: 用户令牌

### 18. 获取我的已审核商品
- **接口**: GET /grouppurchase/getMyGoodPriceFinishList
- **说明**: 获取当前用户已审核通过的商品列表
- **参数**: 同上

### 19. 删除我的商品
- **接口**: GET /grouppurchase/delMyGoodPrice
- **说明**: 删除自己发布的商品
- **参数**:
  - goodpriceid: 商品ID
  - uid: 用户ID
  - token: 用户令牌

## 认证说明

需要认证的接口必须在请求头中包含Authorization字段:
```
Authorization: Bearer your_token_here
```

或在请求参数中包含token和uid:
```
token: your_token_here
uid: user_id
```

## 测试数据

系统已预置测试数据:
- 测试用户: testuser1, testuser2
- 测试商品: iPhone 15 Pro Max, MacBook Air M2, 小米13 Ultra
- 测试评论和收藏数据

## 启动服务

1. 安装依赖: `pip install -r requirements.txt`
2. 运行启动脚本: `./start.sh`
3. 或者直接运行: `python run.py`

服务将在 http://localhost:5000 启动
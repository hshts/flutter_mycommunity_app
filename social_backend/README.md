# 社交电商平台后端项目

这是一个基于Flask框架的现代社交电商平台后端项目，提供了完整的社交和电商功能。

## 项目结构

```
social_ecommerce_backend/
├── app/                  # 应用主目录
│   ├── __init__.py       # 应用初始化
│   ├── models/           # 数据模型
│   ├── fields/           # API模型定义（使用flask-restx）
│   ├── controllers/      # 请求处理控制器
│   ├── services/         # 业务逻辑服务
│   ├── utils/            # 工具函数
│   ├── middleware/       # 中间件
│   └── config.py         # 配置文件
├── migrations/           # 数据库迁移文件
├── tests/                # 测试文件
├── requirements.txt      # 依赖包
└── run.py                # 应用入口
```

## 设计模式

本项目采用分层架构设计：

1. **Controllers（控制器层）**：处理HTTP请求和响应，参数验证，调用Service层
2. **Services（服务层）**：实现业务逻辑，处理数据操作，事务管理
3. **Models（模型层）**：定义数据结构，与数据库交互
4. **Fields（字段层）**：使用flask-restx定义API模型和文档
5. **Utils（工具层）**：通用工具函数
6. **Middleware（中间件层）**：请求和响应的预处理和后处理

这种分层架构的优势：
- 职责分离，代码结构清晰
- 易于测试和维护
- 提高代码复用性
- 便于团队协作开发

## API文档

本项目使用flask-restx自动生成API文档，可以通过以下URL访问：
- API文档: http://localhost:5000/doc/

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python run.py
```

## 运行测试

1. 运行所有测试：
```bash
pytest
```

2. 运行特定测试文件：
```bash
pytest tests/test_activity.py
```

3. 运行特定测试方法：
```bash
pytest tests/test_activity.py::TestActivity::test_create_activity
```

## 已实现的模块

### Activity 模块

Activity模块提供了完整的活动管理功能，包括：

1. 创建活动 (`/Activity/createActivity`)
2. 获取活动详情 (`/Activity/getActivity`)
3. 根据更新时间获取活动列表 (`/Activity/getActivityListByUpdateTime`)
4. 根据用户获取活动列表 (`/Activity/getActivityListByUser`)
5. 获取用户参与的活动列表 (`/Activity/getJoinActivityListByUser`)
6. 活动点赞 (`/Activity/updateLike`)
7. 活动取消点赞 (`/Activity/delLike`)
8. 活动收藏 (`/Activity/updateCollection`)
9. 活动取消收藏 (`/Activity/delCollection`)
10. 发布活动评论 (`/Activity/updatecomment`)
11. 删除活动评论 (`/Activity/delcomment`)
12. 参加活动 (`/Activity/joinActivity`)
13. 删除活动 (`/Activity/delActivity`)
14. 更新活动时间 (`/Activity/updateActivityTime`)
15. 更新活动信息 (`/Activity/updateActivity`)
16. 更新活动状态 (`/Activity/updateActivityStatus`)
17. 退出活动 (`/Activity/exitActivity`)
18. 获取群聊信息 (`/Activity/getGroupConversation`)

## 数据模型

### Activity 模型

参考 [flutter_model.md](../flutter_model.md) 中的Activity模型定义，我们实现了以下字段：

- actid: 活动ID
- content: 活动内容
- createtime: 创建时间
- updatetime: 更新时间
- status: 活动状态
- peoplenum: 活动总人数
- currentpeoplenum: 当前参与人数
- startyear: 开始时间戳
- endyear: 结束时间戳
- address: 活动地址
- addresstitle: 地址标题
- lat: 纬度
- lng: 经度
- actcity: 活动城市
- actprovince: 活动省份
- coverimg: 封面图片
- coverimgwh: 封面图片宽高比
- actimagespath: 活动图片路径列表
- maxcost: 最大费用
- mincost: 最小费用
- paytype: 支付类型
- uid: 发起人用户ID
- goodpriceid: 关联商品ID
- likenum: 点赞数
- collectionnum: 收藏数
- commentnum: 评论数
- viewnum: 浏览数
- joinnum: 参与数
- locked: 是否锁定(活动开始)

## API 接口

所有接口遵循 [community_api.md](../community_api.md) 中定义的规范，包括请求路径、方法、输入参数和输出结果。

## 认证

使用 JWT 进行用户认证。需要认证的接口会在请求头中添加 `Authorization: Bearer <token>`。

## 测试

为每个API接口编写了单元测试，使用pytest框架和factory-boy库来生成测试数据。

测试用例覆盖了以下场景：
1. 正常流程测试
2. 边界条件测试
3. 异常情况测试
4. 数据库状态验证

## 下一步计划

1. 实现 Group Purchase 模块
2. 实现 User 模块
3. 实现 IM 模块
4. 添加数据库迁移支持
5. 添加 API 文档
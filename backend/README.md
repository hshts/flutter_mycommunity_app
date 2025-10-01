# 社交电商团购后端服务

基于Flutter前端项目的Flask后端API服务，主要提供团购商品相关的服务接口。与Flutter前端的GPService完全对应，实现了25+个API接口。

## 项目特点

✅ **完整对应**: 与Flutter前端GPService的25+个方法完全对应  
✅ **RESTful API**: 标准的HTTP API接口设计  
✅ **数据库支持**: SQLAlchemy ORM，支持SQLite/MySQL/PostgreSQL  
✅ **跨域支持**: 内置CORS支持，解决前端跨域问题  
✅ **认证系统**: 基于Token的用户认证  
✅ **测试数据**: 预置完整测试数据，开箱即用  

## 项目结构

```
backend/
├── app/
│   ├── __init__.py          # Flask应用初始化
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── good_price.py    # 好价商品模型 (对应GoodPiceModel)
│   │   ├── comment.py       # 评论模型 (对应Comment)
│   │   ├── activity.py      # 活动模型 (对应Activity)
│   │   ├── user.py          # 用户模型
│   │   └── collection.py    # 收藏和点赞模型
│   ├── routes/              # 路由控制器
│   │   ├── __init__.py
│   │   └── grouppurchase.py # 团购API路由 (25+个接口)
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   └── gp_service.py    # 团购业务服务
│   └── utils/               # 工具类
│       ├── __init__.py
│       ├── response.py      # 统一响应格式化
│       └── auth.py          # 认证工具
├── config.py                # 配置文件 (开发/生产环境)
├── requirements.txt         # Python依赖包
├── run.py                   # 服务启动入口
├── init_data.py            # 测试数据初始化
├── start.sh                # 一键启动脚本
├── API.md                  # 详细API文档
└── README.md               # 项目说明
```

## 核心功能模块

### 🛍️ 团购商品管理
- **商品搜索**: 关键词搜索、热门搜索、推荐搜索
- **商品筛选**: 地区筛选、分类筛选、价格排序
- **商品详情**: 完整商品信息展示，浏览计数
- **商品发布**: 用户发布商品，支持图片上传
- **商品管理**: 我的商品列表，待审核/已审核状态

### 💬 评论互动系统
- **发表评论**: 支持商品评论和评论回复
- **评论管理**: 删除自己的评论和回复
- **点赞系统**: 评论点赞/取消点赞，实时统计
- **用户信息**: 评论显示用户头像和昵称

### ❤️ 收藏点赞功能
- **商品收藏**: 收藏/取消收藏商品
- **收藏列表**: 用户收藏商品列表查看
- **商品点赞**: 好价商品点赞/取消点赞
- **统计数据**: 收藏数、点赞数实时更新

### 🏃 活动管理 (预留)
- 团购活动创建和参与
- 活动状态管理
- 订单生成和支付

## 快速开始

### 1. 环境要求
- Python 3.7+
- Flask 2.0+
- SQLAlchemy 1.4+

### 2. 一键启动
```bash
cd backend
./start.sh
```

### 3. 手动启动
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库和测试数据
python init_data.py

# 3. 启动服务
python run.py
```

### 4. 访问服务
- **服务地址**: http://localhost:5000
- **健康检查**: http://localhost:5000/health
- **API接口**: http://localhost:5000/grouppurchase/
- **API文档**: 查看 API.md

## API接口概览

与Flutter前端GPService的25+个方法完全对应：

| 分类 | 接口数量 | 主要功能 |
|------|----------|----------|
| 搜索相关 | 3个 | 热门搜索、推荐搜索、商品搜索 |
| 收藏相关 | 4个 | 收藏、取消收藏、收藏列表 |
| 评论相关 | 6个 | 评论增删、回复、点赞 |
| 商品相关 | 8个 | 商品详情、推荐列表、我的商品 |
| 点赞相关 | 4个 | 商品点赞、评论点赞及取消 |

详细API文档请查看 [API.md](API.md)

## 测试数据

系统预置了完整的测试数据：

### 测试用户
- **testuser1**: 测试用户1 (13800138001)
- **testuser2**: 测试用户2 (13800138002)

### 测试商品
- **iPhone 15 Pro Max**: ¥8999 (热门推荐)
- **MacBook Air M2**: ¥7999 (推荐商品)  
- **小米13 Ultra**: ¥4999 (热门商品)

### 测试评论
每个商品都有相应的测试评论和回复数据

## 配置说明

### 数据库配置
```python
# 开发环境 (默认SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_community.db'

# 生产环境
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/community'
```

### 跨域配置
```python
# 开发环境允许所有来源
CORS_ORIGINS = ["*"]

# 生产环境指定域名
CORS_ORIGINS = ["https://yourdomain.com"]
```

## 与Flutter前端的对应关系

| Flutter方法 | 后端接口 | 功能说明 |
|-------------|----------|----------|
| `hotsearchProduct()` | `GET /hotsearchProduct` | 获取热门搜索 |
| `getRecommendSearchProduct()` | `POST /getRecommendSearchProduct` | 推荐搜索 |
| `updateGoodPriceCollection()` | `POST /updateGoodPriceCollection` | 收藏商品 |
| `getUserGoodPriceCollectionInfo()` | `GET /getUserGoodPriceCollectionInfo` | 收藏列表 |
| `updateComment()` | `POST /updatecomment` | 添加评论 |
| `getCommentList()` | `GET /getcomment` | 获取评论 |
| `searchProduct()` | `POST /searchProduct` | 搜索商品 |
| `getGoodPriceInfo()` | `GET /getGoodPriceInfo` | 商品详情 |
| ... | ... | 25+个接口完全对应 |

## 开发计划

- [x] 核心商品管理API
- [x] 评论系统API  
- [x] 收藏点赞API
- [x] 搜索推荐API
- [x] 用户认证系统
- [x] 测试数据和文档
- [ ] 活动管理功能完善
- [ ] 支付订单系统
- [ ] 图片上传功能
- [ ] 消息推送系统

## 技术栈

- **Web框架**: Flask 2.3+
- **数据库ORM**: SQLAlchemy 1.4+
- **跨域处理**: Flask-CORS
- **数据序列化**: 自定义to_dict方法
- **认证方式**: Token-based认证
- **数据库**: SQLite (开发) / MySQL (生产)

## 部署建议

### 开发环境
```bash
python run.py
```

### 生产环境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 使用uWSGI
pip install uwsgi
uwsgi --http :5000 --module run:app
```

## 贡献指南

1. Fork本项目
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

## 许可证

MIT License
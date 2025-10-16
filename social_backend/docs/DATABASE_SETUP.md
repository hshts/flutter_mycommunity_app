# 数据库初始化和使用指南

## 问题说明

当你看到错误 `no such table: activities` 时，说明数据库表还没有创建。

## 解决方案

### 1. 初始化数据库

运行以下命令创建数据库表：

```bash
python init_db.py
```

这将：
- 删除旧表（如果存在）
- 创建新的 activities 表
- 显示表结构

### 2. 添加测试数据

运行以下命令添加一些测试数据：

```bash
python add_test_data.py
```

这将添加5个测试活动：
- 3个深圳市的活动 (citycode: 440300)
- 1个福田区的活动 (citycode: 440304)
- 1个北京市的活动 (citycode: 110100)

### 3. 启动应用

```bash
flask run
```

或

```bash
python run.py
```

### 4. 测试 API

#### 使用浏览器
访问 Swagger 文档：
```
http://localhost:5000/doc
```

#### 使用 curl

获取深圳的活动：
```bash
curl "http://localhost:5000/Activity/getActivityListByCity?citycode=440300"
```

获取福田区的活动：
```bash
curl "http://localhost:5000/Activity/getActivityListByCity?citycode=440304"
```

按点赞数排序：
```bash
curl "http://localhost:5000/Activity/getActivityListByCity?citycode=440300&orderBy=likenum"
```

#### 使用 Python 测试脚本
```bash
python scripts/test_city_api.py
```

## 常用命令

### 重置数据库
如果需要重新开始：
```bash
# 1. 初始化数据库（会删除所有数据）
python init_db.py

# 2. 添加测试数据
python add_test_data.py
```

### 查看数据库
使用 SQLite 命令行工具：
```bash
sqlite3 app.db

# 查看所有表
.tables

# 查看 activities 表结构
.schema activities

# 查看所有活动
SELECT actid, content, actcity FROM activities;

# 退出
.quit
```

### 检查数据
使用 Python：
```python
from api import create_app, db
from api.models.activity import Activity

app = create_app()
with app.app_context():
    # 查看总数
    print(f"Total activities: {Activity.query.count()}")
    
    # 查看深圳的活动
    sz_activities = Activity.query.filter_by(actcity='440300').all()
    for act in sz_activities:
        print(f"- {act.content}")
```

## 测试数据说明

添加的测试数据包含：

| 活动名称 | 城市代码 | 点赞数 | 浏览数 | 参与人数 |
|---------|---------|--------|--------|---------|
| 深圳周末户外徒步活动 | 440300 | 125 | 2580 | 8 |
| 深圳湾骑行活动 | 440300 | 89 | 1850 | 12 |
| 南山科技园周末羽毛球活动 | 440300 | 56 | 980 | 6 |
| 福田中心区周末跑步团 | 440304 | 178 | 3120 | 15 |
| 北京周末爬香山活动 | 110100 | 234 | 4520 | 18 |

## 故障排查

### 问题：数据库文件被锁定
```bash
# 停止所有 Flask 进程
pkill -f "flask run"

# 重新初始化
python init_db.py
```

### 问题：表已存在但结构不对
```bash
# 删除数据库文件
rm app.db

# 重新初始化
python init_db.py
python add_test_data.py
```

### 问题：需要保留数据
如果你需要保留现有数据，使用 Flask-Migrate：
```bash
# 初始化迁移（仅首次）
flask db init

# 创建迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

## 生产环境

在生产环境中：

1. **不要使用** `init_db.py`（会删除所有数据）
2. **使用** Flask-Migrate 进行数据库迁移
3. **使用** 环境变量配置数据库连接
4. **定期备份** 数据库

生产环境配置示例：
```bash
# .env 文件
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

## 相关文件

- `init_db.py` - 数据库初始化脚本
- `add_test_data.py` - 测试数据添加脚本
- `api/models/activity.py` - Activity 模型定义
- `api/config.py` - 数据库配置
- `app.db` - SQLite 数据库文件

## 更多帮助

查看完整的 API 文档：
```bash
cat docs/API_getActivityListByCity.md
```

运行所有测试：
```bash
pytest tests/test_activity.py -v
```

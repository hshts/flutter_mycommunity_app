# Group Purchase 字段重命名说明

## 更改内容

将 `GoodPrice` 模型中的 `imgs` 字段重命名为 `albumpics`（相册图片）。

## 字段说明

| 原字段名 | 新字段名 | 数据类型 | 说明 |
|---------|---------|---------|------|
| imgs    | albumpics | TEXT | 商品相册图片列表 |

## 修改的文件

### 1. 模型定义
**文件**: `api/models/group_purchase.py`

```python
# 修改前
imgs = db.Column(db.Text)  # 图片列表

# 修改后
albumpics = db.Column(db.Text)  # 图片列表
```

### 2. 服务层
**文件**: `api/services/group_purchase_service.py`

修改了以下方法：
- `create_good_price()` - 创建商品时使用 `albumpics`
- `update_good_price()` - 更新商品时使用 `albumpics`

```python
# 创建商品
albumpics=data.get('albumpics'),

# 更新商品
if 'albumpics' in data:
    good_price.albumpics = data['albumpics']
```

### 3. 控制器层
**文件**: `api/controllers/group_purchase.py`

更新了请求模型定义：

```python
create_good_price_model = ns.model('CreateGoodPrice', {
    ...
    'albumpics': fields.String(description='图片列表'),
    ...
})
```

## 数据库迁移

### 迁移步骤
1. 创建新表结构（包含 `albumpics` 字段）
2. 将旧表数据迁移到新表（`imgs` -> `albumpics`）
3. 删除旧表
4. 重命名新表

### 迁移脚本
```bash
python rename_imgs_to_albumpics.py
```

### 迁移结果
- ✓ 成功迁移 6 条记录
- ✓ 字段类型：TEXT
- ✓ 数据完整性验证通过

## API 使用示例

### 创建商品
```json
POST /grouppurchase/createGoodPrice
{
    "token": "user_token",
    "uid": 1001,
    "title": "商品标题",
    "content": "商品详情",
    "albumpics": "[\"pic1.jpg\",\"pic2.jpg\",\"pic3.jpg\"]",
    "pic": "cover.jpg",
    "price": 99.0,
    ...
}
```

### 更新商品
```json
POST /grouppurchase/updateGoodPrice
{
    "token": "user_token",
    "goodpriceid": "xxx",
    "uid": 1001,
    "albumpics": "[\"new_pic1.jpg\",\"new_pic2.jpg\"]",
    ...
}
```

### 响应示例
```json
{
    "success": true,
    "data": {
        "goodpriceid": "xxx",
        "title": "商品标题",
        "albumpics": "[\"pic1.jpg\",\"pic2.jpg\"]",
        "pic": "cover.jpg",
        ...
    }
}
```

## 数据格式建议

### JSON 字符串格式
推荐使用 JSON 数组字符串格式存储多张图片：

```json
"[\"https://example.com/pic1.jpg\",\"https://example.com/pic2.jpg\"]"
```

### 逗号分隔格式
也可以使用简单的逗号分隔格式：

```
"pic1.jpg,pic2.jpg,pic3.jpg"
```

## 前端集成

### Flutter 示例
```dart
// 解析 albumpics
List<String> parseAlbumPics(String? albumpics) {
  if (albumpics == null || albumpics.isEmpty) {
    return [];
  }
  
  // 尝试解析 JSON 格式
  try {
    return List<String>.from(jsonDecode(albumpics));
  } catch (e) {
    // 如果不是 JSON，按逗号分隔
    return albumpics.split(',').map((s) => s.trim()).toList();
  }
}

// 使用示例
final good = goodPriceData;
final albumPics = parseAlbumPics(good['albumpics']);

// 显示图片列表
GridView.builder(
  itemCount: albumPics.length,
  itemBuilder: (context, index) {
    return Image.network(albumPics[index]);
  },
)
```

## 字段命名说明

### 为什么使用 `albumpics`？

1. **语义更清晰**: `albumpics` 明确表示"相册图片"，比 `imgs` 更具描述性
2. **区分主图**: 与 `pic`（主图/封面图）形成对比，清晰区分单图和多图
3. **符合命名规范**: 使用完整单词组合，避免过度缩写
4. **国际化**: `album` 是通用的相册概念，易于理解

### 字段关系

```
GoodPrice
├── pic         - 主图/封面图（单张）
└── albumpics   - 相册图片（多张）
```

## 验证测试

### 测试项目
- ✓ 数据库表结构正确（albumpics 为 TEXT 类型）
- ✓ 模型定义正确（移除 imgs，添加 albumpics）
- ✓ to_dict() 方法正确返回 albumpics
- ✓ 数据查询功能正常
- ✓ 数据更新功能正常
- ✓ API 功能完整测试通过

### 测试脚本
```bash
# 验证字段重命名
python verify_albumpics_field.py

# 完整功能测试
python test_group_purchase.py
```

## 注意事项

1. **向后兼容**: 旧的 `imgs` 字段已完全移除，API 不再接受该字段
2. **数据格式**: 建议统一使用 JSON 数组字符串格式
3. **前端适配**: 前端需要更新字段名从 `imgs` 到 `albumpics`
4. **文档更新**: 所有 API 文档需要更新字段名称

## 相关文件

- `api/models/group_purchase.py` - 模型定义
- `api/services/group_purchase_service.py` - 服务层
- `api/controllers/group_purchase.py` - 控制器层
- `rename_imgs_to_albumpics.py` - 数据库迁移脚本
- `verify_albumpics_field.py` - 验证脚本

## 测试结果

✓ 字段重命名成功
✓ 数据迁移完成（6条记录）
✓ 所有功能测试通过
✓ API 接口正常工作

更新时间: 2025-10-15

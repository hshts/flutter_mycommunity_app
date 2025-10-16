# Group Purchase 模块分类字段更改说明

## 更改内容

将 `GoodPrice` 模型中的 `category` 字段从 `String(100)` 类型改为 `Integer` 类型。

## 分类代码定义

| 代码 | 分类名称 | 说明 |
|-----|---------|------|
| 1   | 生鲜水果 | 新鲜水果、蔬菜等生鲜类商品 |
| 2   | 餐饮美食 | 餐厅、外卖、饮品等餐饮类商品 |
| 3   | 日用百货 | 日常生活用品、清洁用品等 |
| 4   | 运动户外 | 运动器材、户外装备等 |
| 5   | 数码电子 | 手机、电脑、耳机等数码产品 |
| 6   | 美妆护肤 | 化妆品、护肤品等美妆类商品 |
| 7   | 服装鞋包 | 服装、鞋子、包包等 |
| 8   | 家居家装 | 家具、装修材料等 |
| 9   | 母婴用品 | 婴儿用品、儿童玩具等 |
| 10  | 图书文娱 | 书籍、文具、娱乐产品等 |
| 99  | 其他     | 其他未分类商品 |

## 数据库更改

### 修改的文件
1. `api/models/group_purchase.py` - 模型定义
   - `category = db.Column(db.String(100))` → `category = db.Column(db.Integer)`

2. `add_group_purchase_test_data.py` - 测试数据
   - 将所有分类从字符串改为整数代码

### 数据迁移步骤

1. **重建数据库表**
   ```bash
   python rebuild_group_purchase_db.py
   ```
   这将删除旧的团购表并创建新表（category为Integer类型）

2. **添加测试数据**
   ```bash
   python add_group_purchase_test_data.py
   ```
   添加使用整数分类代码的测试数据

3. **验证更改**
   ```bash
   python verify_category_field.py
   ```
   验证category字段类型和数据正确性

## API 使用示例

### 创建商品
```json
POST /grouppurchase/createGoodPrice
{
    "token": "user_token",
    "uid": 1001,
    "title": "商品标题",
    "content": "商品详情",
    "category": 1,  // 使用整数代码
    "price": 99.0,
    ...
}
```

### 搜索商品（按分类过滤）
```python
# Service层示例
goods = GoodPrice.query.filter_by(category=1, status=1).all()  # 查询生鲜水果分类
```

## 前端集成

前端需要维护分类代码映射表：

```dart
// Flutter 示例
final Map<int, String> categoryMap = {
  1: '生鲜水果',
  2: '餐饮美食',
  3: '日用百货',
  4: '运动户外',
  5: '数码电子',
  6: '美妆护肤',
  7: '服装鞋包',
  8: '家居家装',
  9: '母婴用品',
  10: '图书文娱',
  99: '其他',
};

String getCategoryName(int code) {
  return categoryMap[code] ?? '未知分类';
}
```

## 优势

1. **性能提升**: Integer类型比String类型查询更快
2. **存储优化**: Integer占用空间更小（4字节 vs 可变长度）
3. **数据一致性**: 避免字符串拼写错误
4. **易于扩展**: 添加新分类只需要添加代码映射
5. **支持国际化**: 分类名称可以根据语言环境动态显示

## 注意事项

1. 所有API请求和响应中的 `category` 字段现在都是整数类型
2. 前端需要维护分类代码到名称的映射表
3. 添加新分类时需要更新文档和前端映射表
4. 建议使用 1-98 作为正常分类，99 作为"其他"分类

## 相关文件

- `api/models/group_purchase.py` - 模型定义
- `api/services/group_purchase_service.py` - 业务逻辑
- `api/controllers/group_purchase.py` - API控制器
- `rebuild_group_purchase_db.py` - 数据库重建脚本
- `add_group_purchase_test_data.py` - 测试数据脚本
- `verify_category_field.py` - 验证脚本

## 测试结果

✓ 数据库表结构正确（category 为 INTEGER 类型）
✓ 测试数据添加成功（6个商品，涵盖6个不同分类）
✓ API功能正常（搜索、筛选、创建等）
✓ 分类统计正确

更新时间: 2025-10-15

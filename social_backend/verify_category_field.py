"""验证 category 字段类型"""
from api import create_app, db

def verify_category_field():
    """验证 category 字段为 Integer 类型"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("验证 GoodPrice.category 字段类型")
        print("=" * 60)
        
        # 1. 检查表结构
        print("\n1. 数据库表结构:")
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('good_prices')
        
        for col in columns:
            if col['name'] == 'category':
                print(f"   字段名: {col['name']}")
                print(f"   数据类型: {col['type']}")
                print(f"   可为空: {col['nullable']}")
                print(f"   默认值: {col['default']}")
                
                if 'INTEGER' in str(col['type']).upper():
                    print("   ✓ 类型正确: INTEGER")
                else:
                    print(f"   ✗ 类型错误: {col['type']}")
                break
        
        # 2. 查询实际数据
        print("\n2. 实际数据验证:")
        result = db.session.execute(
            db.text('SELECT goodpriceid, title, category FROM good_prices LIMIT 5')
        )
        
        category_names = {
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
            99: '其他'
        }
        
        for row in result:
            goodpriceid, title, category = row
            category_name = category_names.get(category, '未知')
            print(f"   • {title[:30]}")
            print(f"     ID: {goodpriceid[:8]}...")
            print(f"     分类: {category} ({category_name})")
            print(f"     分类类型: {type(category).__name__}")
            print()
        
        # 3. 统计分类分布
        print("3. 分类分布统计:")
        result = db.session.execute(
            db.text('SELECT category, COUNT(*) as cnt FROM good_prices GROUP BY category ORDER BY category')
        )
        
        for row in result:
            category, count = row
            category_name = category_names.get(category, '未知')
            print(f"   分类 {category:2d} ({category_name:8s}): {count} 个商品")
        
        print("\n" + "=" * 60)
        print("✓ 验证完成!")
        print("=" * 60)

if __name__ == '__main__':
    verify_category_field()

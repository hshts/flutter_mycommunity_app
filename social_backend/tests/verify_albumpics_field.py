"""验证 albumpics 字段"""
from api import create_app, db
from api.models import GoodPrice

def verify_albumpics_field():
    """验证 albumpics 字段"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("验证 albumpics 字段")
        print("=" * 60)
        
        # 1. 检查表结构
        print("\n1. 数据库表结构:")
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('good_prices')
        
        for col in columns:
            if col['name'] in ['albumpics', 'pic', 'imgs']:
                print(f"   • {col['name']}: {col['type']}")
        
        # 2. 检查模型定义
        print("\n2. 模型定义检查:")
        if hasattr(GoodPrice, 'albumpics'):
            print("   ✓ GoodPrice 模型有 'albumpics' 属性")
        else:
            print("   ✗ GoodPrice 模型缺少 'albumpics' 属性")
        
        if hasattr(GoodPrice, 'imgs'):
            print("   ! GoodPrice 模型仍有 'imgs' 属性")
        else:
            print("   ✓ GoodPrice 模型已移除 'imgs' 属性")
        
        # 3. 测试查询
        print("\n3. 测试数据查询:")
        goods = GoodPrice.query.limit(3).all()
        
        for good in goods:
            print(f"\n   • {good.title}")
            print(f"     goodpriceid: {good.goodpriceid[:16]}...")
            print(f"     albumpics: {good.albumpics if good.albumpics else '(空)'}")
            print(f"     pic: {good.pic if good.pic else '(空)'}")
            
            # 测试 to_dict()
            good_dict = good.to_dict()
            if 'albumpics' in good_dict:
                print(f"     ✓ to_dict() 包含 'albumpics'")
            else:
                print(f"     ✗ to_dict() 缺少 'albumpics'")
            
            if 'imgs' in good_dict:
                print(f"     ! to_dict() 仍包含 'imgs'")
        
        # 4. 测试更新
        print("\n4. 测试字段更新:")
        first_good = GoodPrice.query.first()
        if first_good:
            test_pics = "pic1.jpg,pic2.jpg,pic3.jpg"
            first_good.albumpics = test_pics
            db.session.commit()
            
            # 重新查询验证
            db.session.refresh(first_good)
            if first_good.albumpics == test_pics:
                print(f"   ✓ albumpics 更新成功")
                print(f"     值: {first_good.albumpics}")
            else:
                print(f"   ✗ albumpics 更新失败")
        
        print("\n" + "=" * 60)
        print("✓ 验证完成!")
        print("=" * 60)

if __name__ == '__main__':
    verify_albumpics_field()

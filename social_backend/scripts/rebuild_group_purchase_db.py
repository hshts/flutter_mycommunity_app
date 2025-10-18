"""重建团购模块数据库表（category改为Integer）"""
from api import create_app, db
from api.models import GoodPrice
import os

def rebuild_group_purchase_tables():
    """重建团购模块数据库表"""
    app = create_app()
    
    with app.app_context():
        print("重建团购模块数据库表...")
        print("注意: 这将删除所有现有的团购数据!")
        
        # 备份提示
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        print(f"\n数据库文件: {db_path}")
        
        confirm = input("\n是否继续? (输入 'yes' 确认): ")
        if confirm.lower() != 'yes':
            print("操作已取消")
            return
        
        try:
            # 删除团购相关表
            print("\n删除旧表...")
            tables_to_drop = [
                'good_prices',
                'good_price_collections',
                'good_price_likes',
                'good_price_comments',
                'good_price_comment_replies',
                'good_price_comment_likes',
                'sku_stocks',
                'group_purchase_orders'
            ]
            
            for table in tables_to_drop:
                try:
                    db.session.execute(db.text(f'DROP TABLE IF EXISTS {table}'))
                    print(f"  ✓ 删除表: {table}")
                except Exception as e:
                    print(f"  ! 跳过表 {table}: {e}")
            
            db.session.commit()
            
            # 重新创建表
            print("\n创建新表...")
            db.create_all()
            
            # 验证表结构
            print("\n验证表结构:")
            inspector = db.inspect(db.engine)
            
            if 'good_prices' in inspector.get_table_names():
                columns = inspector.get_columns('good_prices')
                category_col = next((c for c in columns if c['name'] == 'category'), None)
                
                if category_col:
                    print(f"  ✓ category 字段类型: {category_col['type']}")
                    if 'INTEGER' in str(category_col['type']).upper():
                        print("  ✓ category 已成功改为 INTEGER 类型!")
                    else:
                        print(f"  ✗ category 类型不正确: {category_col['type']}")
                else:
                    print("  ✗ 未找到 category 字段")
            
            print("\n✓ 数据库表重建完成!")
            print("\n分类代码说明:")
            print("  1: 生鲜水果")
            print("  2: 餐饮美食")
            print("  3: 日用百货")
            print("  4: 运动户外")
            print("  5: 数码电子")
            print("  6: 美妆护肤")
            print("  7: 服装鞋包")
            print("  8: 家居家装")
            print("  9: 母婴用品")
            print("  10: 图书文娱")
            print("  99: 其他")
            
        except Exception as e:
            print(f"\n✗ 操作失败: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    rebuild_group_purchase_tables()

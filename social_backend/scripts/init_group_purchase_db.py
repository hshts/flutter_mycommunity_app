"""初始化团购模块数据库表

运行此脚本以创建团购相关的数据库表
"""
from api import create_app, db
from api.models import (
    GoodPrice, GoodPriceCollection, GoodPriceLike,
    GoodPriceComment, GoodPriceCommentReply, GoodPriceCommentLike,
    SkuStock, GroupPurchaseOrder
)

def init_group_purchase_tables():
    """初始化团购模块数据库表"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 显示创建的表信息
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("✓ 数据库表创建成功!")
        print("\n已创建的表:")
        for table in tables:
            print(f"  - {table}")
            
            # 显示表结构
            columns = inspector.get_columns(table)
            print(f"    字段数: {len(columns)}")
            for col in columns:
                print(f"      • {col['name']}: {col['type']}")
            print()

if __name__ == '__main__':
    init_group_purchase_tables()

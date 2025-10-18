"""初始化商品评价表"""
from api import create_app, db
from api.models import GoodPriceEvaluate, GoodPriceEvaluateReply, GoodPriceEvaluateLike

def init_evaluate_tables():
    """初始化评价相关表"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("初始化商品评价表")
        print("=" * 60)
        
        # 创建所有表
        db.create_all()
        
        # 显示创建的表信息
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        evaluate_tables = [
            'good_price_evaluates',
            'good_price_evaluate_replies',
            'good_price_evaluate_likes'
        ]
        
        print("\n评价相关表:")
        for table in evaluate_tables:
            if table in tables:
                print(f"  ✓ {table}")
                columns = inspector.get_columns(table)
                print(f"    字段数: {len(columns)}")
                for col in columns:
                    print(f"      • {col['name']}: {col['type']}")
                print()
            else:
                print(f"  ✗ {table} (未找到)")
        
        print("=" * 60)
        print("✓ 评价表初始化完成!")
        print("=" * 60)

if __name__ == '__main__':
    init_evaluate_tables()

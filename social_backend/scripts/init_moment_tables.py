"""初始化动态(Moment)相关表"""
from api import create_app, db
from api.models.moment import (
    Moment, MomentComment, MomentCommentReply,
    MomentLike, MomentCommentLike
)

def init_moment_tables():
    """初始化动态相关表"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("初始化动态(Moment)相关表")
        print("=" * 60)
        
        # 创建表
        print("\n1. 创建数据表...")
        Moment.__table__.create(db.engine, checkfirst=True)
        print("   ✓ moments 表创建成功")
        
        MomentComment.__table__.create(db.engine, checkfirst=True)
        print("   ✓ moment_comments 表创建成功")
        
        MomentCommentReply.__table__.create(db.engine, checkfirst=True)
        print("   ✓ moment_comment_replies 表创建成功")
        
        MomentLike.__table__.create(db.engine, checkfirst=True)
        print("   ✓ moment_likes 表创建成功")
        
        MomentCommentLike.__table__.create(db.engine, checkfirst=True)
        print("   ✓ moment_comment_likes 表创建成功")
        
        # 验证表结构
        print("\n2. 验证表结构:")
        inspector = db.inspect(db.engine)
        
        tables = [
            'moments',
            'moment_comments',
            'moment_comment_replies',
            'moment_likes',
            'moment_comment_likes'
        ]
        
        for table_name in tables:
            if inspector.has_table(table_name):
                columns = inspector.get_columns(table_name)
                print(f"   ✓ {table_name}: {len(columns)} 个字段")
            else:
                print(f"   ✗ {table_name}: 表不存在")
        
        print("\n" + "=" * 60)
        print("✅ 动态表初始化完成!")
        print("=" * 60)

if __name__ == '__main__':
    init_moment_tables()

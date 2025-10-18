"""初始化活动评论相关数据库表"""
from api import create_app, db
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike

def init_comment_tables():
    """初始化评论相关表"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("初始化活动评论相关数据库表")
        print("=" * 60)
        
        # 创建表
        db.create_all()
        
        print("\n✓ 创建表成功:")
        print("  1. activity_comments (活动评论表)")
        print("  2. activity_comment_replies (活动评论回复表)")
        print("  3. activity_comment_likes (活动评论点赞表)")
        
        # 显示表结构
        print("\n" + "=" * 60)
        print("表结构详情:")
        print("=" * 60)
        
        # ActivityComment 表结构
        print("\n1. activity_comments:")
        for column in ActivityComment.__table__.columns:
            print(f"   - {column.name}: {column.type}")
        
        # ActivityCommentReply 表结构
        print("\n2. activity_comment_replies:")
        for column in ActivityCommentReply.__table__.columns:
            print(f"   - {column.name}: {column.type}")
        
        # ActivityCommentLike 表结构
        print("\n3. activity_comment_likes:")
        for column in ActivityCommentLike.__table__.columns:
            print(f"   - {column.name}: {column.type}")
        
        print("\n" + "=" * 60)
        print("✓ 数据库表初始化完成!")
        print("=" * 60)

if __name__ == '__main__':
    init_comment_tables()

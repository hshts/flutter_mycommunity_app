"""重建评论表 - 将commentid从String改为Integer"""
from api import create_app, db
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike

def rebuild_comment_tables():
    """重建评论相关表结构"""
    app = create_app()
    
    with app.app_context():
        print("开始重建评论表...")
        
        # 1. 删除旧表
        print("1. 删除旧表...")
        ActivityCommentLike.__table__.drop(db.engine, checkfirst=True)
        ActivityCommentReply.__table__.drop(db.engine, checkfirst=True)
        ActivityComment.__table__.drop(db.engine, checkfirst=True)
        print("   旧表已删除")
        
        # 2. 创建新表
        print("2. 创建新表(Integer类型的commentid)...")
        ActivityComment.__table__.create(db.engine, checkfirst=True)
        ActivityCommentReply.__table__.create(db.engine, checkfirst=True)
        ActivityCommentLike.__table__.create(db.engine, checkfirst=True)
        print("   新表已创建")
        
        # 3. 验证表结构
        print("\n3. 验证新表结构:")
        inspector = db.inspect(db.engine)
        
        for table_name in ['activity_comments', 'activity_comment_replies', 'activity_comment_likes']:
            columns = inspector.get_columns(table_name)
            print(f"\n   表 {table_name}:")
            for col in columns:
                if 'id' in col['name']:
                    print(f"   - {col['name']}: {col['type']} (primary={col.get('primary_key', False)}, auto={col.get('autoincrement', False)})")
        
        print("\n✅ 评论表重建完成!")
        print("⚠️  注意: 所有旧的测试数据已被清除")
        print("💡 提示: 运行 python add_comment_test_data.py 重新生成测试数据")

if __name__ == '__main__':
    rebuild_comment_tables()

"""验证commentid已经改为Integer类型"""
from api import create_app, db
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike
from sqlalchemy import inspect

def verify_integer_commentid():
    """验证commentid字段类型"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("验证 commentid 字段类型")
        print("=" * 70)
        
        inspector = inspect(db.engine)
        
        # 1. 检查数据库表结构
        print("\n【1】数据库表结构检查:")
        print("-" * 70)
        
        tables_to_check = {
            'activity_comments': ['commentid', 'replyid', 'likeid'],
            'activity_comment_replies': ['replyid', 'commentid'],
            'activity_comment_likes': ['likeid', 'commentid']
        }
        
        for table_name, id_columns in tables_to_check.items():
            print(f"\n表: {table_name}")
            columns = inspector.get_columns(table_name)
            
            for col in columns:
                if any(id_col in col['name'] for id_col in id_columns):
                    col_type = str(col['type'])
                    is_int = 'INTEGER' in col_type
                    status = "✅" if is_int else "❌"
                    print(f"  {status} {col['name']}: {col_type} "
                          f"(Primary: {col.get('primary_key', False)}, "
                          f"AutoIncrement: {col.get('autoincrement', 'default')})")
        
        # 2. 检查实际数据
        print("\n" + "=" * 70)
        print("【2】实际数据检查:")
        print("-" * 70)
        
        # 检查评论
        comments = ActivityComment.query.limit(5).all()
        print(f"\n✓ 找到 {ActivityComment.query.count()} 条评论")
        print("\n前5条评论的ID类型和值:")
        for comment in comments:
            print(f"  - commentid: {comment.commentid} (类型: {type(comment.commentid).__name__})")
        
        # 检查回复
        replies = ActivityCommentReply.query.limit(5).all()
        print(f"\n✓ 找到 {ActivityCommentReply.query.count()} 条回复")
        print("\n前5条回复的ID类型和值:")
        for reply in replies:
            print(f"  - replyid: {reply.replyid} (类型: {type(reply.replyid).__name__}), "
                  f"commentid: {reply.commentid} (类型: {type(reply.commentid).__name__})")
        
        # 检查点赞
        likes = ActivityCommentLike.query.limit(5).all()
        print(f"\n✓ 找到 {ActivityCommentLike.query.count()} 条点赞")
        print("\n前5条点赞的ID类型和值:")
        for like in likes:
            print(f"  - likeid: {like.likeid} (类型: {type(like.likeid).__name__}), "
                  f"commentid: {like.commentid} (类型: {type(like.commentid).__name__})")
        
        # 3. 验证外键关系
        print("\n" + "=" * 70)
        print("【3】外键关系验证:")
        print("-" * 70)
        
        if comments:
            comment = comments[0]
            replies = ActivityCommentReply.query.filter_by(commentid=comment.commentid).all()
            likes = ActivityCommentLike.query.filter_by(commentid=comment.commentid).all()
            
            print(f"\n评论ID {comment.commentid} (Integer类型):")
            print(f"  ✓ 关联的回复数: {len(replies)}")
            print(f"  ✓ 关联的点赞数: {len(likes)}")
            
            if replies:
                print(f"  ✓ 回复ID示例: {[r.replyid for r in replies[:3]]}")
            if likes:
                print(f"  ✓ 点赞ID示例: {[l.likeid for l in likes[:3]]}")
        
        # 4. 最终总结
        print("\n" + "=" * 70)
        print("【4】验证总结:")
        print("-" * 70)
        
        all_checks = []
        
        # 检查所有commentid字段是否为INTEGER
        for table_name in ['activity_comments', 'activity_comment_replies', 'activity_comment_likes']:
            columns = inspector.get_columns(table_name)
            for col in columns:
                if 'commentid' in col['name']:
                    is_integer = 'INTEGER' in str(col['type'])
                    all_checks.append(is_integer)
                    status = "✅" if is_integer else "❌"
                    print(f"\n{status} {table_name}.{col['name']}: "
                          f"{'INTEGER (正确)' if is_integer else 'STRING (错误)'}")
        
        # 检查所有主键是否为INTEGER且自增
        for table_name, id_col in [('activity_comments', 'commentid'), 
                                     ('activity_comment_replies', 'replyid'),
                                     ('activity_comment_likes', 'likeid')]:
            columns = inspector.get_columns(table_name)
            for col in columns:
                if col['name'] == id_col and col.get('primary_key'):
                    is_integer = 'INTEGER' in str(col['type'])
                    all_checks.append(is_integer)
                    status = "✅" if is_integer else "❌"
                    print(f"{status} {table_name}.{id_col}: "
                          f"{'INTEGER主键 (正确)' if is_integer else '非INTEGER主键 (错误)'}")
        
        print("\n" + "=" * 70)
        if all(all_checks):
            print("✅ 所有字段类型验证通过！commentid已成功改为Integer类型")
        else:
            print("❌ 部分字段类型验证失败！")
        print("=" * 70)

if __name__ == '__main__':
    verify_integer_commentid()

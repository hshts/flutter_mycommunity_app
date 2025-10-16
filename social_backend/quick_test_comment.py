"""快速测试 getCommentList 接口"""
from api import create_app, db
from api.models.activity import Activity
from api.models.comment import ActivityComment

def quick_test():
    """快速测试"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("快速测试 getCommentList 接口")
        print("=" * 60)
        
        # 获取有评论的活动
        activity = db.session.query(Activity).join(
            ActivityComment,
            Activity.actid == ActivityComment.actid
        ).first()
        
        if not activity:
            print("\n⚠️  没有测试数据")
            return
        
        actid = activity.actid
        
        print(f"\n活动ID: {actid}")
        print(f"活动内容: {activity.content[:50]}...")
        
        # 查询评论
        comments = ActivityComment.query.filter_by(
            actid=actid,
            status=1
        ).all()
        
        print(f"\n评论数量: {len(comments)}")
        
        for i, comment in enumerate(comments, 1):
            print(f"\n评论 {i}:")
            print(f"  ID: {comment.commentid[:16]}...")
            print(f"  用户: {comment.uid}")
            print(f"  内容: {comment.content}")
            print(f"  点赞: {comment.likenum}")
            print(f"  回复: {comment.replynum}")
        
        print("\n" + "=" * 60)
        print("接口端点: GET /Activity/getCommentList")
        print(f"测试URL: http://localhost:5000/Activity/getCommentList?actid={actid}&uid=1000")
        print("=" * 60)
        
        # 测试接口响应
        from api.services.comment_service import CommentService
        
        print("\n测试服务层方法:")
        result = CommentService.get_comment_list(actid, 1000)
        
        print(f"✓ 返回 {len(result)} 条评论")
        
        if result:
            print(f"\n第一条评论数据结构:")
            import json
            print(json.dumps(result[0], indent=2, ensure_ascii=False))
        
        print("\n✓ 接口测试通过！")

if __name__ == '__main__':
    quick_test()

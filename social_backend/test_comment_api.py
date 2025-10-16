"""测试活动评论 API 接口"""
from api import create_app, db
from api.models.activity import Activity
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike
from api.services.comment_service import CommentService
import json

def test_comment_api():
    """测试评论相关 API"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("测试活动评论 API 接口")
        print("=" * 60)
        
        # 1. 获取有评论的活动
        print("\n1. 查询有评论的活动:")
        activities_with_comments = db.session.query(Activity).join(
            ActivityComment,
            Activity.actid == ActivityComment.actid
        ).distinct().limit(3).all()
        
        if not activities_with_comments:
            print("   ⚠️  没有找到有评论的活动")
            return
        
        print(f"   找到 {len(activities_with_comments)} 个有评论的活动")
        
        for activity in activities_with_comments:
            comment_count = ActivityComment.query.filter_by(
                actid=activity.actid,
                status=1
            ).count()
            print(f"   • {activity.content[:30]}...: {comment_count} 条评论")
        
        # 2. 测试 getCommentList 接口
        test_activity = activities_with_comments[0]
        print(f"\n2. 测试 getCommentList 接口:")
        print(f"   活动: {test_activity.content[:50]}...")
        print(f"   活动ID: {test_activity.actid[:16]}...")
        
        # 获取评论列表
        comments = CommentService.get_comment_list(test_activity.actid, uid=1000)
        
        print(f"\n   返回 {len(comments)} 条评论:")
        for i, comment in enumerate(comments, 1):
            print(f"\n   评论 {i}:")
            print(f"     评论ID: {comment['commentid'][:16]}...")
            print(f"     用户: {comment['user']['username']}")
            print(f"     内容: {comment['content'][:40]}...")
            print(f"     点赞数: {comment['likenum']}")
            print(f"     回复数: {comment['replynum']}")
            print(f"     是否点赞: {comment.get('isLiked', False)}")
            print(f"     创建时间: {comment['createtime'][:19]}")
        
        # 3. 测试 getReplyList 接口
        if comments:
            test_comment = comments[0]
            print(f"\n3. 测试 getReplyList 接口:")
            print(f"   评论ID: {test_comment['commentid'][:16]}...")
            
            replies = CommentService.get_reply_list(test_comment['commentid'])
            
            if replies:
                print(f"\n   返回 {len(replies)} 条回复:")
                for i, reply in enumerate(replies, 1):
                    print(f"\n   回复 {i}:")
                    print(f"     回复ID: {reply['replyid'][:16]}...")
                    print(f"     用户: {reply['user']['username']}")
                    print(f"     回复给: {reply['touser']['username']}")
                    print(f"     内容: {reply['content'][:40]}...")
                    print(f"     创建时间: {reply['createtime'][:19]}")
            else:
                print("   该评论暂无回复")
        
        # 4. 测试 getNewCommentList 接口
        print(f"\n4. 测试 getNewCommentList 接口:")
        if comments:
            # 获取第一条评论之后的新评论
            first_comment_id = comments[0]['commentid']
            new_comments = CommentService.get_new_comment_list(
                test_activity.actid,
                first_comment_id
            )
            
            print(f"   从评论 {first_comment_id[:16]}... 之后的新内容:")
            print(f"   返回 {len(new_comments)} 条新内容")
            
            for item in new_comments[:3]:
                print(f"\n   类型: {item['type']}")
                print(f"     用户: {item['user']['username']}")
                print(f"     内容: {item['content'][:30]}...")
        
        # 5. 测试 getReply 接口
        print(f"\n5. 测试 getReply 接口:")
        all_replies = ActivityCommentReply.query.filter_by(status=1).first()
        if all_replies:
            reply_detail = CommentService.get_reply(all_replies.replyid)
            if reply_detail:
                print(f"   回复ID: {reply_detail['replyid'][:16]}...")
                print(f"   用户: {reply_detail['user']['username']}")
                print(f"   回复给: {reply_detail['touser']['username']}")
                print(f"   内容: {reply_detail['content']}")
                print(f"   创建时间: {reply_detail['createtime'][:19]}")
        
        # 6. 测试 getCommentReplyList 接口
        print(f"\n6. 测试 getCommentReplyList 接口:")
        test_uid = 1000
        user_replies = CommentService.get_comment_reply_list(test_uid)
        
        print(f"   用户 {test_uid} 收到的回复:")
        print(f"   返回 {len(user_replies)} 条回复")
        
        for i, reply in enumerate(user_replies[:3], 1):
            print(f"\n   回复 {i}:")
            print(f"     来自: {reply['user']['username']}")
            print(f"     内容: {reply['content'][:30]}...")
            if 'activity' in reply:
                print(f"     活动: {reply['activity']['content'][:30]}...")
        
        # 7. 测试评论点赞功能
        print(f"\n7. 测试评论点赞功能:")
        if comments:
            test_comment_id = comments[0]['commentid']
            test_like_uid = 9999
            
            # 点赞
            success = CommentService.add_comment_like(
                test_comment_id,
                test_like_uid,
                comments[0]['uid'],
                test_activity.actid
            )
            
            if success:
                print(f"   ✓ 用户 {test_like_uid} 点赞成功")
                
                # 验证点赞数增加
                comment = ActivityComment.query.get(test_comment_id)
                print(f"   ✓ 评论点赞数已更新: {comment.likenum}")
                
                # 取消点赞
                success = CommentService.remove_comment_like(test_comment_id, test_like_uid)
                if success:
                    print(f"   ✓ 取消点赞成功")
                    db.session.refresh(comment)
                    print(f"   ✓ 评论点赞数已更新: {comment.likenum}")
        
        # 8. 统计信息
        print(f"\n8. 评论数据统计:")
        total_comments = ActivityComment.query.filter_by(status=1).count()
        total_replies = ActivityCommentReply.query.filter_by(status=1).count()
        total_likes = ActivityCommentLike.query.count()
        
        print(f"   总评论数: {total_comments}")
        print(f"   总回复数: {total_replies}")
        print(f"   总点赞数: {total_likes}")
        
        # 按活动统计
        print(f"\n   各活动评论分布:")
        for activity in activities_with_comments:
            comment_count = ActivityComment.query.filter_by(
                actid=activity.actid,
                status=1
            ).count()
            reply_count = db.session.query(ActivityCommentReply).join(
                ActivityComment,
                ActivityCommentReply.commentid == ActivityComment.commentid
            ).filter(
                ActivityComment.actid == activity.actid,
                ActivityCommentReply.status == 1
            ).count()
            
            print(f"   • {activity.content[:30]}...: {comment_count} 评论, {reply_count} 回复")
        
        # 9. JSON 序列化测试
        print(f"\n9. JSON 序列化测试:")
        response_data = {
            'data': comments[:2],
            'count': len(comments)
        }
        
        try:
            json_str = json.dumps(response_data, indent=2, ensure_ascii=False)
            print("   ✓ JSON 序列化成功")
            print(f"   JSON 大小: {len(json_str)} 字节")
        except Exception as e:
            print(f"   ✗ JSON 序列化失败: {e}")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成!")
        print("=" * 60)
        
        # 10. API 调用示例
        print("\n10. API 调用示例:")
        print("\n   GET /Activity/getCommentList?actid={actid}&uid={uid}")
        print("   响应:")
        print("   {")
        print('     "data": [')
        print('       {')
        print('         "commentid": "评论ID",')
        print('         "actid": "活动ID",')
        print('         "uid": 1000,')
        print('         "content": "评论内容",')
        print('         "likenum": 5,')
        print('         "replynum": 2,')
        print('         "isLiked": true,')
        print('         "user": {')
        print('           "uid": 1000,')
        print('           "username": "用户1000",')
        print('           "profilepicture": "头像URL"')
        print('         }')
        print('       }')
        print('     ],')
        print('     "count": 10')
        print("   }")
        
        print("\n   GET /Activity/getReplyList?commentid={commentid}")
        print("   响应:")
        print("   {")
        print('     "data": [')
        print('       {')
        print('         "replyid": "回复ID",')
        print('         "commentid": "评论ID",')
        print('         "uid": 2000,')
        print('         "touid": 1000,')
        print('         "content": "回复内容",')
        print('         "user": {...},')
        print('         "touser": {...}')
        print('       }')
        print('     ],')
        print('     "count": 5')
        print("   }")

if __name__ == '__main__':
    test_comment_api()

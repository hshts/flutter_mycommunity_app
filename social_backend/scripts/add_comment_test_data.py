"""添加活动评论测试数据"""
import os
import sys

# 将项目根目录加入到模块搜索路径，确保可以导入 api 包
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api import create_app, db
from api.models.activity import Activity
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike
from api.services.comment_service import CommentService
from datetime import datetime, timedelta
import random

def add_comment_test_data():
    """添加评论测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("添加活动评论测试数据")
        print("=" * 60)
        
        # 1. 获取活动列表
        activities = Activity.query.limit(3).all()
        
        if not activities:
            print("\n⚠️  数据库中没有活动，请先创建活动")
            return
        
        print(f"\n找到 {len(activities)} 个活动，开始添加评论...")
        
        comments_data = []
        replies_data = []
        
        # 2. 为每个活动添加评论
        for activity in activities:
            print(f"\n为活动 '{activity.content[:30]}...' 添加评论:")
            
            # 添加 3-5 条评论
            num_comments = random.randint(3, 5)
            activity_comments = []
            
            for i in range(num_comments):
                uid = 1000 + i
                content_options = [
                    "这个活动看起来很有趣！",
                    "什么时候开始啊？期待！",
                    "地点在哪里呢？",
                    "报名参加！期待见到大家",
                    "活动组织得很棒，给个赞！",
                    "有什么要求吗？新人可以参加吗？",
                    "上次的活动很精彩，这次一定要来！",
                    "想了解更多细节，有详细介绍吗？"
                ]
                
                comment_data = {
                    'actid': activity.actid,
                    'uid': uid,
                    'content': random.choice(content_options)
                }
                
                commentid = CommentService.add_comment(comment_data)
                comments_data.append({
                    'commentid': commentid,
                    'actid': activity.actid,
                    'uid': uid,
                    'content': comment_data['content']
                })
                activity_comments.append(commentid)
                print(f"  ✓ 添加评论 {i+1}: 用户{uid} - {comment_data['content'][:20]}...")
            
            # 3. 为部分评论添加回复
            num_replies = min(2, len(activity_comments))
            for i in range(num_replies):
                commentid = activity_comments[i]
                reply_data = {
                    'commentid': commentid,
                    'actid': activity.actid,
                    'uid': 2000 + i,  # 不同的用户回复
                    'touid': 1000 + i,  # 回复给评论的用户
                    'content': random.choice([
                        "感谢关注！活动详情已更新在描述中",
                        "欢迎新朋友加入！没有特殊要求",
                        "你好！可以查看活动详情了解更多",
                        "谢谢支持！期待你的参与"
                    ])
                }
                
                replyid = CommentService.add_comment_reply(reply_data)
                replies_data.append({
                    'replyid': replyid,
                    'commentid': commentid,
                    'uid': reply_data['uid'],
                    'touid': reply_data['touid'],
                    'content': reply_data['content']
                })
                print(f"  ✓ 添加回复: 用户{reply_data['uid']} 回复给 用户{reply_data['touid']}")
            
            # 4. 为部分评论添加点赞
            num_likes = min(3, len(activity_comments))
            for i in range(num_likes):
                commentid = activity_comments[i]
                like_uid = 3000 + i
                likeuid = 1000 + i  # 被点赞的用户
                
                CommentService.add_comment_like(commentid, like_uid, likeuid, activity.actid)
                print(f"  ✓ 用户{like_uid} 点赞了评论")
        
        # 5. 统计信息
        print("\n" + "=" * 60)
        print("数据统计:")
        print("=" * 60)
        
        total_comments = ActivityComment.query.count()
        total_replies = ActivityCommentReply.query.count()
        total_likes = ActivityCommentLike.query.count()
        
        print(f"\n总评论数: {total_comments}")
        print(f"总回复数: {total_replies}")
        print(f"总点赞数: {total_likes}")
        
        # 6. 显示部分数据示例
        print("\n" + "=" * 60)
        print("数据示例:")
        print("=" * 60)
        
        for activity in activities[:2]:
            comments = ActivityComment.query.filter_by(actid=activity.actid).all()
            print(f"\n活动: {activity.content[:30]}...")
            print(f"  评论数: {len(comments)}")
            
            for comment in comments[:2]:
                print(f"\n  评论ID: {comment.commentid}")
                print(f"    用户: {comment.uid}")
                print(f"    内容: {comment.content}")
                print(f"    点赞数: {comment.likenum}")
                print(f"    回复数: {comment.replynum}")
                
                # 显示回复
                replies = ActivityCommentReply.query.filter_by(commentid=comment.commentid).all()
                if replies:
                    print(f"    回复:")
                    for reply in replies:
                        print(f"      - 用户{reply.uid} 回复 用户{reply.touid}: {reply.content[:30]}...")
        
        print("\n" + "=" * 60)
        print("✓ 测试数据添加完成!")
        print("=" * 60)

if __name__ == '__main__':
    add_comment_test_data()

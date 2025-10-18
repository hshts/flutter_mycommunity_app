"""生成动态(Moment)测试数据"""
import os
import sys

# 将项目根目录加入到模块搜索路径，确保可以导入 api 包
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api import create_app, db
from api.models.moment import Moment, MomentComment, MomentCommentReply, MomentLike, MomentCommentLike
from api.services.moment_service import MomentService
import random
import json

def add_moment_test_data():
    """添加动态测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("添加动态(Moment)测试数据")
        print("=" * 60)
        
        # 测试用户ID列表
        test_uids = [1000, 1001, 1002, 1003, 1004]
        
        # 测试分类/话题
        categories = ['生活分享', '旅行', '美食', '运动健身', '摄影', '读书', '音乐', '电影']
        
        # 测试动态内容
        moment_contents = [
            '今天天气真好,出去走走~',
            '分享一下最近的生活状态',
            '周末愉快!大家有什么计划吗?',
            '这个地方真的太美了!',
            '推荐一家超棒的餐厅',
            '打卡网红景点',
            '健身第30天,继续加油!',
            '读完了一本好书,很有收获',
            '最近爱上了摄影',
            '分享我的音乐歌单'
        ]
        
        # 测试评论内容
        comment_contents = [
            '太棒了!',
            '赞同!',
            '说得好!',
            '我也想去试试',
            '羡慕啊',
            '加油!',
            '真不错',
            '学习了',
            '感谢分享',
            '期待更新'
        ]
        
        # 测试回复内容
        reply_contents = [
            '谢谢支持!',
            '一起加油!',
            '欢迎交流',
            '后续会继续分享的',
            '感谢关注',
            '握手!'
        ]
        
        # 1. 创建动态
        print("\n1. 创建测试动态...")
        moment_ids = []
        
        for i in range(15):
            uid = random.choice(test_uids)
            content = random.choice(moment_contents)
            category = random.choice(categories)
            
            # 随机添加图片
            images = None
            if random.random() > 0.5:
                image_list = [
                    f'https://example.com/images/moment_{i}_1.jpg',
                    f'https://example.com/images/moment_{i}_2.jpg'
                ]
                images = json.dumps(image_list)
            
            momentid = MomentService.create_moment(
                uid=uid,
                content=f"{content} #{category}",
                images=images,
                coverimgwh='16:9' if images else None,
                category=category
            )
            
            moment_ids.append(momentid)
            print(f"   ✓ 创建动态 {momentid}: 用户{uid} - {content[:20]}...")
        
        # 2. 添加点赞
        print("\n2. 添加动态点赞...")
        like_count = 0
        for momentid in moment_ids[:10]:
            # 每个动态随机2-5个点赞
            like_uids = random.sample(test_uids, random.randint(2, 5))
            for like_uid in like_uids:
                MomentService.add_moment_like(momentid, like_uid)
                like_count += 1
        print(f"   ✓ 添加了 {like_count} 个点赞")
        
        # 3. 添加评论
        print("\n3. 添加动态评论...")
        comment_count = 0
        for momentid in moment_ids[:8]:
            # 每个动态随机2-4个评论
            for _ in range(random.randint(2, 4)):
                comment_uid = random.choice(test_uids)
                content = random.choice(comment_contents)
                
                commentid = MomentService.add_moment_comment(
                    momentid=momentid,
                    uid=comment_uid,
                    touid=None,
                    content=content
                )
                comment_count += 1
                
                # 部分评论添加回复
                if random.random() > 0.6:
                    reply_uid = random.choice([u for u in test_uids if u != comment_uid])
                    reply_content = random.choice(reply_contents)
                    
                    MomentService.add_moment_comment(
                        momentid=momentid,
                        uid=reply_uid,
                        touid=comment_uid,
                        content=reply_content,
                        commentid=commentid
                    )
        
        print(f"   ✓ 添加了 {comment_count} 个评论")
        
        # 4. 添加评论点赞
        print("\n4. 添加评论点赞...")
        comment_like_count = 0
        comments = MomentComment.query.limit(10).all()
        for comment in comments:
            # 每个评论随机1-3个点赞
            like_uids = random.sample(test_uids, random.randint(1, 3))
            for like_uid in like_uids:
                try:
                    MomentService.add_moment_comment_like(comment.commentid, like_uid)
                    comment_like_count += 1
                except:
                    pass
        
        print(f"   ✓ 添加了 {comment_like_count} 个评论点赞")
        
        # 5. 统计数据
        print("\n" + "=" * 60)
        print("数据统计")
        print("=" * 60)
        
        total_moments = Moment.query.filter_by(status=1).count()
        total_comments = MomentComment.query.filter_by(status=1).count()
        total_replies = MomentCommentReply.query.filter_by(status=1).count()
        total_moment_likes = MomentLike.query.count()
        total_comment_likes = MomentCommentLike.query.count()
        
        print(f"\n总动态数: {total_moments}")
        print(f"总评论数: {total_comments}")
        print(f"总回复数: {total_replies}")
        print(f"总动态点赞数: {total_moment_likes}")
        print(f"总评论点赞数: {total_comment_likes}")
        
        # 6. 显示示例数据
        print("\n" + "=" * 60)
        print("数据示例")
        print("=" * 60)
        
        moments = Moment.query.filter_by(status=1).limit(3).all()
        for moment in moments:
            print(f"\n动态ID: {moment.momentid}")
            print(f"  用户: {moment.uid}")
            print(f"  内容: {moment.content}")
            print(f"  分类: {moment.category}")
            print(f"  点赞数: {moment.likenum}")
            print(f"  评论数: {moment.commentnum}")
            
            # 显示该动态的评论
            comments = MomentComment.query.filter_by(
                momentid=moment.momentid,
                status=1
            ).limit(2).all()
            
            if comments:
                print(f"  评论:")
                for comment in comments:
                    print(f"    - 用户{comment.uid}: {comment.content} (点赞: {comment.likenum}, 回复: {comment.replynum})")
        
        print("\n" + "=" * 60)
        print("✅ 测试数据添加完成!")
        print("=" * 60)

if __name__ == '__main__':
    add_moment_test_data()

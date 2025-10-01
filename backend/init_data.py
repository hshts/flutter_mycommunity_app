"""
测试数据初始化脚本
运行此脚本来创建一些测试数据
"""

from app import create_app, db
from app.models import GoodPrice, User, Comment, Collection, Like
from datetime import datetime
import json

def init_test_data():
    """初始化测试数据"""
    app = create_app('development')
    
    with app.app_context():
        # 清空现有数据（可选）
        # db.drop_all()
        # db.create_all()
        
        # 创建测试用户
        test_users = [
            User(
                username="testuser1",
                nickname="测试用户1",
                email="test1@example.com",
                phone="13800138001",
                avatar="https://via.placeholder.com/100",
                status=1
            ),
            User(
                username="testuser2", 
                nickname="测试用户2",
                email="test2@example.com",
                phone="13800138002",
                status=1
            )
        ]
        
        for user in test_users:
            existing = User.query.filter_by(username=user.username).first()
            if not existing:
                db.session.add(user)
        
        db.session.commit()
        
        # 创建测试商品
        user1 = User.query.filter_by(username="testuser1").first()
        user2 = User.query.filter_by(username="testuser2").first()
        
        test_goods = [
            GoodPrice(
                title="iPhone 15 Pro Max 256GB",
                desc="全新iPhone 15 Pro Max，钛金属材质，A17 Pro处理器",
                price=8999.0,
                original_price=9999.0,
                image_url="https://via.placeholder.com/300x300",
                platform="苹果官网",
                platform_url="https://www.apple.com.cn",
                category="手机数码",
                tags=json.dumps(["iPhone", "苹果", "手机"]),
                view_count=1200,
                like_count=156,
                comment_count=23,
                collect_count=89,
                status=1,
                is_hot=True,
                is_recommend=True,
                user_id=user1.id if user1 else 1,
                user_name=user1.nickname if user1 else "测试用户",
                user_avatar=user1.avatar if user1 else "",
                location="广东省,深圳市"
            ),
            GoodPrice(
                title="MacBook Air M2 13英寸",
                desc="苹果MacBook Air M2处理器 13英寸笔记本电脑",
                price=7999.0,
                original_price=8999.0,
                image_url="https://via.placeholder.com/300x300",
                platform="京东",
                platform_url="https://www.jd.com",
                category="电脑办公",
                tags=json.dumps(["MacBook", "苹果", "笔记本"]),
                view_count=800,
                like_count=92,
                comment_count=15,
                collect_count=45,
                status=1,
                is_hot=False,
                is_recommend=True,
                user_id=user2.id if user2 else 2,
                user_name=user2.nickname if user2 else "测试用户2",
                user_avatar="",
                location="北京市,北京市"
            ),
            GoodPrice(
                title="小米13 Ultra 徕卡影像",
                desc="小米13 Ultra 徕卡专业影像 骁龙8 Gen2处理器",
                price=4999.0,
                original_price=5999.0,
                image_url="https://via.placeholder.com/300x300",
                platform="小米商城",
                platform_url="https://www.mi.com",
                category="手机数码",
                tags=json.dumps(["小米", "手机", "徕卡"]),
                view_count=600,
                like_count=78,
                comment_count=12,
                collect_count=34,
                status=1,
                is_hot=True,
                is_recommend=False,
                user_id=user1.id if user1 else 1,
                user_name=user1.nickname if user1 else "测试用户",
                user_avatar=user1.avatar if user1 else "",
                location="上海市,上海市"
            )
        ]
        
        for good in test_goods:
            existing = GoodPrice.query.filter_by(title=good.title).first()
            if not existing:
                db.session.add(good)
        
        db.session.commit()
        
        # 创建测试评论
        good1 = GoodPrice.query.filter_by(title="iPhone 15 Pro Max 256GB").first()
        if good1 and user1:
            test_comments = [
                Comment(
                    content="这个价格真的很不错，比官网便宜很多！",
                    good_price_id=good1.id,
                    user_id=user1.id,
                    user_name=user1.nickname,
                    user_avatar=user1.avatar,
                    like_count=5
                ),
                Comment(
                    content="有现货吗？什么时候能发货？",
                    good_price_id=good1.id,
                    user_id=user2.id if user2 else user1.id,
                    user_name=user2.nickname if user2 else user1.nickname,
                    user_avatar="",
                    like_count=2
                )
            ]
            
            for comment in test_comments:
                existing = Comment.query.filter_by(
                    content=comment.content,
                    good_price_id=comment.good_price_id
                ).first()
                if not existing:
                    db.session.add(comment)
        
        db.session.commit()
        print("测试数据初始化完成！")

if __name__ == '__main__':
    init_test_data()
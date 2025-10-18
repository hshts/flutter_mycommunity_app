"""
为 GoodPrice 添加评论测试数据
包括评论、回复、点赞
"""
from api import db, create_app
from api.models.group_purchase import (
    GoodPrice, GoodPriceComment, GoodPriceCommentReply, 
    GoodPriceCommentLike
)
from datetime import datetime, timedelta
import random
import uuid

def add_goodprice_comment_test_data():
    """添加商品评论测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("为 GoodPrice 添加评论测试数据")
        print("=" * 70)
        
        # 获取现有的商品
        good_prices = GoodPrice.query.limit(10).all()
        
        if not good_prices:
            print("\n❌ 没有找到商品数据,请先添加商品数据")
            print("\n💡 提示: 你可能需要先创建一些 GoodPrice 测试数据")
            return
        
        print(f"\n找到 {len(good_prices)} 个商品")
        
        # 测试用户ID列表
        test_uids = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
        
        # 评论内容模板
        comment_contents = [
            "这个价格真的很划算!",
            "已经买了,质量不错",
            "比其他地方便宜好多",
            "求问这个现在还能买吗?",
            "有人拼单吗?",
            "这个品牌怎么样啊?",
            "配送快吗?",
            "包装完好,很满意",
            "性价比很高,推荐!",
            "和图片一样,好评!",
            "优惠力度挺大的",
            "家人们快冲!",
            "刚需可以入",
            "等了好久终于降价了",
            "有优惠券吗?",
            "同款其他店铺更贵",
            "品质很好,值得购买",
            "发货速度很快",
            "客服态度很好",
            "会回购的",
            "物流很快,第二天就到了",
            "包装精美,送礼也合适",
            "用了一段时间,感觉不错",
            "这个活动力度很大",
            "终于等到补货了",
        ]
        
        # 回复内容模板
        reply_contents = [
            "可以的,现在还有货",
            "我也买了,确实不错",
            "可以一起拼单",
            "这个品牌挺好的",
            "一般第二天就到了",
            "同意,性价比很高",
            "我也在用,推荐!",
            "确实很划算",
            "店里还有优惠券可以领",
            "谢谢推荐!",
            "好的,谢谢",
            "我也想知道",
            "已下单,坐等收货",
            "同款比价过了,这里最便宜",
            "质量很好,放心买",
            "我昨天刚收到货",
            "建议等双十一可能更便宜",
            "这个牌子一直在用",
            "已经回购好几次了",
            "客服回复很及时",
        ]
        
        print("\n开始添加测试数据...")
        print("-" * 70)
        
        total_comments = 0
        total_replies = 0
        total_likes = 0
        
        # 为每个商品添加评论
        for idx, good_price in enumerate(good_prices, 1):
            print(f"处理商品 {idx}/{len(good_prices)}: {good_price.title[:40]}...")
            
            # 每个商品随机添加 2-6 条评论
            num_comments = random.randint(2, 6)
            
            for i in range(num_comments):
                # 创建评论
                comment_uid = random.choice(test_uids)
                comment = GoodPriceComment(
                    goodpriceid=good_price.goodpriceid,
                    uid=comment_uid,
                    content=random.choice(comment_contents),
                    likenum=random.randint(0, 25),
                    createtime=datetime.utcnow() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
                )
                db.session.add(comment)
                db.session.flush()  # 获取自动生成的 commentid
                total_comments += 1
                
                # 为部分评论添加回复 (40% 概率)
                if random.random() < 0.4:
                    num_replies = random.randint(1, 3)
                    for j in range(num_replies):
                        reply_uid = random.choice([u for u in test_uids if u != comment_uid])
                        reply = GoodPriceCommentReply(
                            replyid=str(uuid.uuid4()),
                            commentid=comment.commentid,
                            goodpriceid=good_price.goodpriceid,
                            uid=reply_uid,
                            touid=comment_uid,
                            content=random.choice(reply_contents),
                            createtime=comment.createtime + timedelta(hours=random.randint(1, 72))
                        )
                        db.session.add(reply)
                        total_replies += 1
                
                # 为部分评论添加点赞 (60% 概率)
                if random.random() < 0.6:
                    num_likes = random.randint(1, 5)
                    liked_uids = set()
                    
                    for k in range(num_likes):
                        like_uid = random.choice(test_uids)
                        # 避免重复点赞和自己给自己点赞
                        if like_uid not in liked_uids and like_uid != comment_uid:
                            like = GoodPriceCommentLike(
                                commentid=comment.commentid,
                                uid=like_uid,
                                likeuid=comment_uid,
                                goodpriceid=good_price.goodpriceid,
                                createtime=comment.createtime + timedelta(hours=random.randint(1, 48))
                            )
                            db.session.add(like)
                            liked_uids.add(like_uid)
                            total_likes += 1
            
            # 更新商品的评论数
            good_price.commentnum = num_comments
        
        # 提交所有更改
        db.session.commit()
        
        print("\n✅ 测试数据添加完成!")
        print("=" * 70)
        print(f"统计信息:")
        print(f"  📦 商品数量: {len(good_prices)}")
        print(f"  💬 评论总数: {total_comments}")
        print(f"  ↩️  回复总数: {total_replies}")
        print(f"  👍 点赞总数: {total_likes}")
        print(f"  📊 平均每个商品: {total_comments / len(good_prices):.1f} 条评论")
        print("=" * 70)
        
        # 显示一些示例数据
        print("\n📋 数据示例:")
        print("-" * 70)
        
        # 随机选择一个有评论的商品展示
        sample_good_price = random.choice(good_prices)
        print(f"\n🛍️  商品: {sample_good_price.title}")
        print(f"   商品ID: {sample_good_price.goodpriceid}")
        print(f"   价格: ¥{sample_good_price.price}")
        print(f"   评论数: {sample_good_price.commentnum}")
        
        # 获取该商品的评论
        comments = GoodPriceComment.query.filter_by(
            goodpriceid=sample_good_price.goodpriceid
        ).order_by(GoodPriceComment.createtime.desc()).all()
        
        print(f"\n💬 该商品的评论 ({len(comments)} 条):")
        for idx, comment in enumerate(comments[:3], 1):  # 只显示前3条
            print(f"\n  [{idx}] commentid: {comment.commentid} (Integer 类型 ✅)")
            print(f"      用户ID: {comment.uid}")
            print(f"      内容: {comment.content}")
            print(f"      点赞数: {comment.likenum}")
            print(f"      创建时间: {comment.createtime.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 获取回复
            replies = GoodPriceCommentReply.query.filter_by(
                commentid=comment.commentid
            ).order_by(GoodPriceCommentReply.createtime.asc()).all()
            
            if replies:
                print(f"      ↩️  回复 ({len(replies)} 条):")
                for reply in replies:
                    print(f"        - 用户 {reply.uid} -> 用户 {reply.touid}: {reply.content}")
            
            # 获取点赞
            likes = GoodPriceCommentLike.query.filter_by(
                commentid=comment.commentid
            ).all()
            
            if likes:
                print(f"      👍 点赞: {len(likes)} 人 (用户ID: {[like.uid for like in likes]})")
        
        if len(comments) > 3:
            print(f"\n  ... 还有 {len(comments) - 3} 条评论")
        
        print("\n" + "=" * 70)
        print("🎯 API 测试建议:")
        print("=" * 70)
        print(f"\n1. 获取评论列表:")
        print(f"   GET /grouppurchase/getcomment?goodpriceid={sample_good_price.goodpriceid}&uid=1001")
        print(f"\n2. 发布评论:")
        print(f"   POST /grouppurchase/updatecomment")
        print(f'   Body: {{"token": "xxx", "goodpriceid": "{sample_good_price.goodpriceid}", "uid": 1001, "content": "测试评论"}}')
        print(f"\n3. 点赞评论:")
        if comments:
            print(f"   POST /grouppurchase/updateCommentLike")
            print(f'   Body: {{"token": "xxx", "commentid": {comments[0].commentid}, "uid": 1001, "likeuid": {comments[0].uid}, "goodpriceid": "{sample_good_price.goodpriceid}"}}')
        print("\n" + "=" * 70)

if __name__ == '__main__':
    add_goodprice_comment_test_data()

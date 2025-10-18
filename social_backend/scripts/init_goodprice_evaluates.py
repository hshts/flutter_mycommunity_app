"""
为 GoodPrice 添加评价(Evaluate)测试数据
包括评价、回复、点赞
"""
from api import db, create_app
from api.models.group_purchase import (
    GoodPrice, GoodPriceEvaluate, GoodPriceEvaluateReply, 
    GoodPriceEvaluateLike
)
from datetime import datetime, timedelta
import random
import uuid

def add_evaluate_test_data():
    """添加评价测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("为 GoodPrice 添加评价(Evaluate)测试数据")
        print("=" * 70)
        
        # 获取现有的商品
        good_prices = GoodPrice.query.limit(10).all()
        
        if not good_prices:
            print("\n❌ 没有找到商品数据,请先添加商品数据")
            return
        
        print(f"\n找到 {len(good_prices)} 个商品")
        
        # 测试用户ID列表
        test_uids = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
        
        # 评价内容模板
        evaluate_contents = [
            "商品质量非常好，物超所值！",
            "包装很精美，物流速度也很快",
            "和描述一致，很满意的一次购物",
            "性价比高，推荐购买",
            "质量一般，价格还算合理",
            "第二次购买了，一如既往的好",
            "家人很喜欢，会回购",
            "物流很快，商品完好无损",
            "客服态度很好，解答很耐心",
            "超出预期，五星好评！",
            "用了几天才来评价，确实不错",
            "性能稳定，使用体验很好",
            "外观漂亮，做工精细",
            "价格实惠，品质有保证",
            "功能齐全，很实用",
            "送货及时，包装完整",
            "物美价廉，强烈推荐",
            "老顾客了，一直信赖这家店",
            "朋友推荐来买的，没让人失望",
            "整体满意，下次还会来",
        ]
        
        # 回复内容模板
        reply_contents = [
            "感谢您的好评！",
            "很高兴您满意我们的产品",
            "您的支持是我们最大的动力",
            "欢迎下次光临！",
            "我们会继续努力的",
            "感谢您的支持与信任",
            "祝您生活愉快！",
            "有任何问题随时联系客服",
            "期待您的再次光临",
            "谢谢您的认可！",
        ]
        
        print("\n开始添加测试数据...")
        print("-" * 70)
        
        total_evaluates = 0
        total_replies = 0
        total_likes = 0
        
        # 为每个商品添加评价
        for idx, good_price in enumerate(good_prices, 1):
            print(f"处理商品 {idx}/{len(good_prices)}: {good_price.title[:40]}...")
            
            # 每个商品随机添加 3-8 条评价
            num_evaluates = random.randint(3, 8)
            
            for i in range(num_evaluates):
                # 创建评价
                evaluate_uid = random.choice(test_uids)
                liketype = random.choices([5, 4, 3], weights=[0.6, 0.3, 0.1])[0]  # 大部分是好评
                
                evaluate = GoodPriceEvaluate(
                    goodpriceid=good_price.goodpriceid,
                    uid=evaluate_uid,
                    content=random.choice(evaluate_contents),
                    liketype=liketype,
                    likenum=random.randint(0, 30),
                    replynum=0,
                    createtime=datetime.utcnow() - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
                )
                db.session.add(evaluate)
                db.session.flush()  # 获取自动生成的 evaluateid
                total_evaluates += 1
                
                # 为部分评价添加商家回复 (50% 概率)
                if random.random() < 0.5:
                    num_replies = random.randint(1, 2)
                    for j in range(num_replies):
                        reply = GoodPriceEvaluateReply(
                            replyid=str(uuid.uuid4()),
                            evaluateid=evaluate.evaluateid,
                            goodpriceid=good_price.goodpriceid,
                            uid=1000,  # 假设1000是商家账号
                            touid=evaluate_uid,
                            content=random.choice(reply_contents),
                            createtime=evaluate.createtime + timedelta(hours=random.randint(1, 48))
                        )
                        db.session.add(reply)
                        total_replies += 1
                    
                    # 更新回复数
                    evaluate.replynum = num_replies
                
                # 为部分评价添加点赞 (70% 概率)
                if random.random() < 0.7:
                    num_likes = random.randint(1, 6)
                    liked_uids = set()
                    
                    for k in range(num_likes):
                        like_uid = random.choice(test_uids)
                        # 避免重复点赞和自己给自己点赞
                        if like_uid not in liked_uids and like_uid != evaluate_uid:
                            like = GoodPriceEvaluateLike(
                                evaluateid=evaluate.evaluateid,
                                uid=like_uid,
                                likeuid=evaluate_uid,
                                goodpriceid=good_price.goodpriceid,
                                createtime=evaluate.createtime + timedelta(hours=random.randint(1, 72))
                            )
                            db.session.add(like)
                            liked_uids.add(like_uid)
                            total_likes += 1
        
        # 提交所有更改
        db.session.commit()
        
        print("\n✅ 测试数据添加完成!")
        print("=" * 70)
        print(f"统计信息:")
        print(f"  📦 商品数量: {len(good_prices)}")
        print(f"  ⭐ 评价总数: {total_evaluates}")
        print(f"  ↩️  回复总数: {total_replies}")
        print(f"  👍 点赞总数: {total_likes}")
        print(f"  📊 平均每个商品: {total_evaluates / len(good_prices):.1f} 条评价")
        print("=" * 70)
        
        # 显示一些示例数据
        print("\n📋 数据示例:")
        print("-" * 70)
        
        # 随机选择一个有评价的商品展示
        sample_good_price = random.choice(good_prices)
        print(f"\n🛍️  商品: {sample_good_price.title}")
        print(f"   商品ID: {sample_good_price.goodpriceid}")
        print(f"   价格: ¥{sample_good_price.price}")
        
        # 获取该商品的评价
        evaluates = GoodPriceEvaluate.query.filter_by(
            goodpriceid=sample_good_price.goodpriceid
        ).order_by(GoodPriceEvaluate.createtime.desc()).all()
        
        print(f"\n⭐ 该商品的评价 ({len(evaluates)} 条):")
        for idx, evaluate in enumerate(evaluates[:3], 1):  # 只显示前3条
            print(f"\n  [{idx}] evaluateid: {evaluate.evaluateid} (Integer 类型 ✅)")
            print(f"      用户ID: {evaluate.uid}")
            print(f"      评分: {'⭐' * evaluate.liketype} ({evaluate.liketype}星)")
            print(f"      内容: {evaluate.content}")
            print(f"      点赞数: {evaluate.likenum}")
            print(f"      回复数: {evaluate.replynum}")
            print(f"      创建时间: {evaluate.createtime.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 获取回复
            replies = GoodPriceEvaluateReply.query.filter_by(
                evaluateid=evaluate.evaluateid
            ).order_by(GoodPriceEvaluateReply.createtime.asc()).all()
            
            if replies:
                print(f"      ↩️  商家回复:")
                for reply in replies:
                    print(f"        - {reply.content}")
            
            # 获取点赞
            likes = GoodPriceEvaluateLike.query.filter_by(
                evaluateid=evaluate.evaluateid
            ).all()
            
            if likes:
                print(f"      👍 点赞: {len(likes)} 人 (用户ID: {[like.uid for like in likes][:5]}...)")
        
        if len(evaluates) > 3:
            print(f"\n  ... 还有 {len(evaluates) - 3} 条评价")
        
        print("\n" + "=" * 70)
        print("🎯 API 测试建议:")
        print("=" * 70)
        print(f"\n1. 获取评价列表:")
        print(f"   POST /grouppurchase/getEvaluateGoodPriceList")
        print(f'   Body: {{"goodpriceid": "{sample_good_price.goodpriceid}", "currentIndex": 0}}')
        print(f"\n2. 发布评价:")
        print(f"   POST /grouppurchase/addEvaluate")
        print(f'   Body: {{"token": "xxx", "goodpriceid": "{sample_good_price.goodpriceid}", "uid": 1001, "content": "测试评价", "liketype": 5}}')
        print(f"\n3. 评价点赞:")
        if evaluates:
            print(f"   POST /grouppurchase/updateEvaluateLike")
            print(f'   Body: {{"token": "xxx", "evaluateid": {evaluates[0].evaluateid}, "uid": 1001, "likeuid": {evaluates[0].uid}, "goodpriceid": "{sample_good_price.goodpriceid}"}}')
        print("\n" + "=" * 70)

if __name__ == '__main__':
    add_evaluate_test_data()

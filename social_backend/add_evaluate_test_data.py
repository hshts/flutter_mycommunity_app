"""添加商品评价测试数据"""
from api import create_app, db
from api.models import GoodPrice, GoodPriceEvaluate, GoodPriceEvaluateReply
from datetime import datetime, timedelta
import uuid

def add_evaluate_test_data():
    """添加评价测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("添加商品评价测试数据")
        print("=" * 60)
        
        # 获取现有商品
        goods = GoodPrice.query.filter_by(status=1).limit(3).all()
        
        if not goods:
            print("✗ 没有找到已审核通过的商品")
            return
        
        print(f"\n找到 {len(goods)} 个商品，为其添加评价...")
        
        # 评价内容模板
        evaluate_contents = [
            {
                'content': '商品质量很好，价格实惠，非常满意！物流也很快，包装完整。',
                'rating': 5,
                'images': '["https://example.com/eval1_1.jpg","https://example.com/eval1_2.jpg"]'
            },
            {
                'content': '性价比不错，和描述的一样，推荐购买。客服态度也很好。',
                'rating': 5,
                'images': '["https://example.com/eval2_1.jpg"]'
            },
            {
                'content': '东西还可以，就是配送慢了一点，整体满意。',
                'rating': 4,
                'images': None
            },
            {
                'content': '物美价廉，团购真的很划算，已经是第二次购买了！',
                'rating': 5,
                'images': '["https://example.com/eval4_1.jpg","https://example.com/eval4_2.jpg","https://example.com/eval4_3.jpg"]'
            },
            {
                'content': '商品不错，但是感觉可以再便宜一点。总体还行。',
                'rating': 4,
                'images': None
            },
            {
                'content': '非常好的购物体验，商品新鲜，质量上乘，五星好评！',
                'rating': 5,
                'images': '["https://example.com/eval6_1.jpg"]'
            }
        ]
        
        # 回复内容模板
        reply_contents = [
            '感谢您的好评！我们会继续努力提供优质商品和服务。',
            '非常感谢您的支持，欢迎再次光临！',
            '感谢您的反馈，我们会持续改进。',
            '谢谢亲的认可，期待您的下次光临！'
        ]
        
        added_evaluates = 0
        added_replies = 0
        
        # 为每个商品添加评价
        for good in goods:
            print(f"\n• 商品: {good.title[:30]}...")
            print(f"  ID: {good.goodpriceid[:16]}...")
            
            # 每个商品添加2-3个评价
            num_evaluates = 2 if added_evaluates < 4 else 1
            
            for i in range(num_evaluates):
                eval_data = evaluate_contents[added_evaluates % len(evaluate_contents)]
                
                evaluateid = str(uuid.uuid4())
                evaluate = GoodPriceEvaluate(
                    evaluateid=evaluateid,
                    goodpriceid=good.goodpriceid,
                    uid=1000 + added_evaluates,  # 不同的用户
                    content=eval_data['content'],
                    rating=eval_data['rating'],
                    images=eval_data['images'],
                    createtime=datetime.utcnow() - timedelta(days=added_evaluates)
                )
                
                db.session.add(evaluate)
                added_evaluates += 1
                
                print(f"  ✓ 添加评价 (用户{evaluate.uid}): {eval_data['content'][:30]}...")
                
                # 为部分评价添加回复
                if added_evaluates % 2 == 0:
                    replyid = str(uuid.uuid4())
                    reply = GoodPriceEvaluateReply(
                        replyid=replyid,
                        evaluateid=evaluateid,
                        goodpriceid=good.goodpriceid,
                        uid=good.uid,  # 商品发布者回复
                        touid=evaluate.uid,
                        content=reply_contents[added_replies % len(reply_contents)],
                        createtime=datetime.utcnow() - timedelta(days=added_evaluates-1)
                    )
                    
                    db.session.add(reply)
                    evaluate.replynum = 1
                    added_replies += 1
                    
                    print(f"    → 添加回复: {reply.content[:30]}...")
        
        db.session.commit()
        
        # 统计信息
        total_evaluates = GoodPriceEvaluate.query.count()
        total_replies = GoodPriceEvaluateReply.query.count()
        
        print(f"\n" + "=" * 60)
        print("✓ 测试数据添加完成!")
        print(f"  总评价数: {total_evaluates}")
        print(f"  总回复数: {total_replies}")
        
        # 显示每个商品的评价统计
        print(f"\n商品评价统计:")
        for good in goods:
            eval_count = GoodPriceEvaluate.query.filter_by(goodpriceid=good.goodpriceid).count()
            avg_rating = db.session.query(db.func.avg(GoodPriceEvaluate.rating)).filter_by(
                goodpriceid=good.goodpriceid
            ).scalar()
            
            print(f"  • {good.title[:30]}: {eval_count} 条评价, 平均 {avg_rating:.1f} 星")
        
        print("=" * 60)

if __name__ == '__main__':
    add_evaluate_test_data()

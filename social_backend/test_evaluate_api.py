"""测试商品评价 API"""
from api import create_app, db
from api.models import GoodPrice, GoodPriceEvaluate
from api.services.group_purchase_service import GroupPurchaseService

def test_evaluate_api():
    """测试评价相关 API"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("测试商品评价 API")
        print("=" * 60)
        
        # 1. 获取有评价的商品
        print("\n1. 获取有评价的商品:")
        goods_with_evaluates = db.session.query(GoodPrice).join(
            GoodPriceEvaluate,
            GoodPrice.goodpriceid == GoodPriceEvaluate.goodpriceid
        ).distinct().limit(3).all()
        
        print(f"   找到 {len(goods_with_evaluates)} 个有评价的商品")
        
        for good in goods_with_evaluates:
            eval_count = GoodPriceEvaluate.query.filter_by(goodpriceid=good.goodpriceid).count()
            print(f"   • {good.title}: {eval_count} 条评价")
        
        # 2. 测试获取商品评价列表
        if goods_with_evaluates:
            test_good = goods_with_evaluates[0]
            
            print(f"\n2. 测试 getEvaluateGoodPriceList (商品: {test_good.title[:30]})")
            print(f"   商品ID: {test_good.goodpriceid[:16]}...")
            
            # 调用服务层方法
            evaluates = GroupPurchaseService.get_evaluate_list(test_good.goodpriceid, current_index=0)
            
            print(f"   找到 {len(evaluates)} 条评价:")
            
            for i, evaluate in enumerate(evaluates, 1):
                print(f"\n   评价 {i}:")
                print(f"     评价ID: {evaluate.evaluateid[:16]}...")
                print(f"     用户ID: {evaluate.uid}")
                print(f"     评分: {'⭐' * evaluate.rating} ({evaluate.rating}/5)")
                print(f"     内容: {evaluate.content[:50]}...")
                print(f"     点赞数: {evaluate.likenum}")
                print(f"     回复数: {evaluate.replynum}")
                print(f"     创建时间: {evaluate.createtime.strftime('%Y-%m-%d %H:%M')}")
                
                if evaluate.images:
                    print(f"     图片: {evaluate.images[:50]}...")
                
                # 获取该评价的回复
                replies = GroupPurchaseService.get_evaluate_replies(evaluate.evaluateid)
                if replies:
                    print(f"     回复列表:")
                    for reply in replies:
                        print(f"       → 用户{reply.uid}: {reply.content[:40]}...")
        
        # 3. 测试添加评价
        print(f"\n3. 测试添加新评价:")
        if goods_with_evaluates:
            test_good = goods_with_evaluates[0]
            
            new_evaluate_data = {
                'goodpriceid': test_good.goodpriceid,
                'uid': 9999,
                'content': '这是一条测试评价，商品非常棒！',
                'rating': 5,
                'images': '["test1.jpg","test2.jpg"]'
            }
            
            evaluateid = GroupPurchaseService.add_evaluate(new_evaluate_data)
            print(f"   ✓ 添加评价成功")
            print(f"   评价ID: {evaluateid[:16]}...")
            
            # 验证评价
            new_evaluate = GroupPurchaseService.get_evaluate(evaluateid)
            if new_evaluate:
                print(f"   ✓ 验证成功: {new_evaluate.content[:30]}...")
        
        # 4. 测试添加评价回复
        print(f"\n4. 测试添加评价回复:")
        first_evaluate = GoodPriceEvaluate.query.first()
        if first_evaluate:
            reply_data = {
                'evaluateid': first_evaluate.evaluateid,
                'goodpriceid': first_evaluate.goodpriceid,
                'uid': 8888,
                'touid': first_evaluate.uid,
                'content': '感谢您的评价，我们会继续努力！'
            }
            
            replyid = GroupPurchaseService.add_evaluate_reply(reply_data)
            print(f"   ✓ 添加回复成功")
            print(f"   回复ID: {replyid[:16]}...")
            
            # 验证回复数更新
            db.session.refresh(first_evaluate)
            print(f"   ✓ 评价回复数已更新: {first_evaluate.replynum}")
        
        # 5. 测试评价点赞
        print(f"\n5. 测试评价点赞:")
        if first_evaluate:
            success = GroupPurchaseService.add_evaluate_like(
                evaluateid=first_evaluate.evaluateid,
                uid=7777,
                likeuid=first_evaluate.uid,
                goodpriceid=first_evaluate.goodpriceid
            )
            
            if success:
                print(f"   ✓ 点赞成功")
                db.session.refresh(first_evaluate)
                print(f"   ✓ 点赞数已更新: {first_evaluate.likenum}")
        
        # 6. 统计信息
        print(f"\n6. 评价统计信息:")
        total_evaluates = GoodPriceEvaluate.query.count()
        total_5_star = GoodPriceEvaluate.query.filter_by(rating=5).count()
        total_4_star = GoodPriceEvaluate.query.filter_by(rating=4).count()
        
        avg_rating = db.session.query(db.func.avg(GoodPriceEvaluate.rating)).scalar()
        
        print(f"   总评价数: {total_evaluates}")
        print(f"   5星评价: {total_5_star} ({total_5_star/total_evaluates*100:.1f}%)")
        print(f"   4星评价: {total_4_star} ({total_4_star/total_evaluates*100:.1f}%)")
        print(f"   平均评分: {avg_rating:.2f} 星")
        
        # 按商品统计
        print(f"\n   商品评价分布:")
        goods = GoodPrice.query.filter_by(status=1).all()
        for good in goods:
            eval_count = GoodPriceEvaluate.query.filter_by(goodpriceid=good.goodpriceid).count()
            if eval_count > 0:
                avg = db.session.query(db.func.avg(GoodPriceEvaluate.rating)).filter_by(
                    goodpriceid=good.goodpriceid
                ).scalar()
                print(f"   • {good.title[:30]}: {eval_count} 条 (平均 {avg:.1f}★)")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成!")
        print("=" * 60)

if __name__ == '__main__':
    test_evaluate_api()

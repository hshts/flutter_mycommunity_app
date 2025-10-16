"""快速测试团购模块 API"""
from api import create_app, db
from api.models import GoodPrice
from api.services.group_purchase_service import GroupPurchaseService

def test_group_purchase_apis():
    """测试团购模块各种功能"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("团购模块 API 测试")
        print("=" * 60)
        
        # 1. 测试获取推荐商品列表
        print("\n1. 测试获取推荐商品列表 (深圳)")
        goods = GroupPurchaseService.get_recommend_good_price_list(
            citycode='440300',
            current_index=0,
            page_size=5
        )
        print(f"   找到 {len(goods)} 个商品")
        for good in goods[:3]:
            print(f"   • {good.title} - ¥{good.price}")
        
        # 2. 测试搜索商品
        print("\n2. 测试搜索商品 (关键词: 团购)")
        goods = GroupPurchaseService.search_product(
            content='团购',
            ordertype='price',
            citycode='440300',
            current_index=0
        )
        print(f"   找到 {len(goods)} 个商品")
        for good in goods:
            print(f"   • {good.title} - ¥{good.price}")
        
        # 3. 测试获取商品详情
        print("\n3. 测试获取商品详情")
        first_good = GoodPrice.query.filter_by(status=1).first()
        if first_good:
            good = GroupPurchaseService.get_good_price(first_good.goodpriceid)
            print(f"   商品: {good.title}")
            print(f"   ID: {good.goodpriceid}")
            print(f"   价格: ¥{good.price} (原价: ¥{good.originalprice})")
            print(f"   折扣: {good.discount}折")
            print(f"   浏览数: {good.viewnum}")
            print(f"   点赞数: {good.likenum}")
            print(f"   收藏数: {good.collectionnum}")
            print(f"   评论数: {good.commentnum}")
        
        # 4. 测试收藏功能
        print("\n4. 测试收藏功能")
        if first_good:
            success = GroupPurchaseService.add_collection(1001, first_good.goodpriceid)
            print(f"   添加收藏: {'成功' if success else '失败'}")
            
            is_collected = GroupPurchaseService.check_user_collection(1001, first_good.goodpriceid)
            print(f"   检查收藏状态: {'已收藏' if is_collected else '未收藏'}")
            
            collections = GroupPurchaseService.get_user_collections(1001, 0, 10)
            print(f"   用户收藏列表: {len(collections)} 个商品")
        
        # 5. 测试点赞功能
        print("\n5. 测试点赞功能")
        if first_good:
            success = GroupPurchaseService.add_like(1001, first_good.goodpriceid)
            print(f"   添加点赞: {'成功' if success else '失败'}")
            
            # 刷新数据
            db.session.refresh(first_good)
            print(f"   当前点赞数: {first_good.likenum}")
        
        # 6. 测试评论功能
        print("\n6. 测试评论功能")
        if first_good:
            comment_data = {
                'goodpriceid': first_good.goodpriceid,
                'uid': 1001,
                'content': '这个商品真不错,价格实惠!'
            }
            commentid = GroupPurchaseService.add_comment(comment_data)
            print(f"   添加评论: 成功 (ID: {commentid[:8]}...)")
            
            comments = GroupPurchaseService.get_comments(first_good.goodpriceid)
            print(f"   评论列表: {len(comments)} 条评论")
            for comment in comments:
                print(f"   • {comment.content[:30]}...")
        
        # 7. 测试按不同条件搜索
        print("\n7. 测试按不同条件搜索")
        
        # 按点赞数排序
        goods_by_like = GroupPurchaseService.search_product(
            content='',
            ordertype='likenum',
            citycode='440300',
            current_index=0,
            page_size=3
        )
        print(f"   按点赞数排序: {len(goods_by_like)} 个商品")
        
        # 按价格排序
        goods_by_price = GroupPurchaseService.search_product(
            content='',
            ordertype='price',
            citycode='440300',
            current_index=0,
            page_size=3
        )
        print(f"   按价格排序: {len(goods_by_price)} 个商品")
        if goods_by_price:
            prices = [g.price for g in goods_by_price]
            print(f"   价格范围: ¥{min(prices)} - ¥{max(prices)}")
        
        # 8. 测试我的商品列表
        print("\n8. 测试我的商品列表")
        my_pending = GroupPurchaseService.get_my_good_price_pending_list(1001)
        print(f"   我的待审核商品: {len(my_pending)} 个")
        
        my_finish = GroupPurchaseService.get_my_good_price_finish_list(1001)
        print(f"   我的已审核商品: {len(my_finish)} 个")
        
        # 9. 统计信息
        print("\n9. 统计信息")
        total_goods = GoodPrice.query.count()
        approved_goods = GoodPrice.query.filter_by(status=1).count()
        pending_goods = GoodPrice.query.filter_by(status=0).count()
        
        print(f"   总商品数: {total_goods}")
        print(f"   已审核通过: {approved_goods}")
        print(f"   待审核: {pending_goods}")
        
        # 按城市统计
        shenzhen_count = GoodPrice.query.filter_by(citycode='440300').count()
        beijing_count = GoodPrice.query.filter_by(citycode='110100').count()
        print(f"   深圳商品: {shenzhen_count}")
        print(f"   北京商品: {beijing_count}")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成!")
        print("=" * 60)

if __name__ == '__main__':
    test_group_purchase_apis()

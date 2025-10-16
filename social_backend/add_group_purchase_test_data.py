"""添加团购模块测试数据"""
from api import create_app, db
from api.models import GoodPrice, SkuStock
from datetime import datetime, timedelta
import uuid

def add_test_good_prices():
    """添加测试商品数据"""
    app = create_app()
    
    with app.app_context():
        # 分类代码定义
        # 1: 生鲜水果, 2: 餐饮美食, 3: 日用百货, 4: 运动户外, 5: 数码电子
        # 6: 美妆护肤, 7: 服装鞋包, 8: 家居家装, 9: 母婴用品, 10: 图书文娱, 99: 其他
        
        # 测试商品数据
        test_goods = [
            {
                'title': '超值团购-新鲜水果拼盘',
                'content': '新鲜当季水果，包含苹果、橙子、香蕉、葡萄等多种水果，适合家庭分享',
                'uid': 1001,
                'productnum': 1,
                'category': 1,  # 生鲜水果
                'brand': '鲜果多',
                'price': 39.9,
                'originalprice': 69.9,
                'totalprice': 39.9,
                'discount': 5.7,
                'province': '广东省',
                'city': '深圳市',
                'citycode': '440300',
                'purchasechannels': '线下门店',
                'address': '南山区科技园',
                'addresstitle': '鲜果多南山店',
                'endtime': datetime.now() + timedelta(days=7),
                'status': 1  # 已审核
            },
            {
                'title': '人气爆款-奶茶套餐',
                'content': '精选茶底，新鲜水果，手工现做奶茶套餐，买一送一限时优惠',
                'uid': 1002,
                'productnum': 2,
                'category': 2,  # 餐饮美食
                'brand': '喜茶',
                'price': 29.9,
                'originalprice': 59.8,
                'totalprice': 29.9,
                'discount': 5.0,
                'province': '广东省',
                'city': '深圳市',
                'citycode': '440300',
                'purchasechannels': '线下门店/外卖',
                'address': '福田区中心城',
                'addresstitle': '喜茶福田店',
                'endtime': datetime.now() + timedelta(days=3),
                'status': 1
            },
            {
                'title': '居家必备-清洁套装',
                'content': '包含洗衣液、洗洁精、消毒液等居家清洁用品，超值组合装',
                'uid': 1001,
                'productnum': 1,
                'category': 3,  # 日用百货
                'brand': '蓝月亮',
                'price': 89.0,
                'originalprice': 150.0,
                'totalprice': 89.0,
                'discount': 5.9,
                'province': '广东省',
                'city': '深圳市',
                'citycode': '440300',
                'purchasechannels': '电商平台',
                'producturl': 'https://example.com/product/123',
                'address': '罗湖区东门',
                'addresstitle': '罗湖仓库',
                'endtime': datetime.now() + timedelta(days=15),
                'status': 1
            },
            {
                'title': '健身必备-运动装备套装',
                'content': '包含瑜伽垫、哑铃、跳绳等健身器材，适合居家锻炼',
                'uid': 1003,
                'productnum': 1,
                'category': 4,  # 运动户外
                'brand': '迪卡侬',
                'price': 199.0,
                'originalprice': 399.0,
                'totalprice': 199.0,
                'discount': 5.0,
                'province': '广东省',
                'city': '深圳市',
                'citycode': '440300',
                'purchasechannels': '线下门店',
                'address': '南山区海岸城',
                'addresstitle': '迪卡侬海岸城店',
                'endtime': datetime.now() + timedelta(days=10),
                'status': 1
            },
            {
                'title': '数码好物-蓝牙耳机',
                'content': '高品质音质，降噪功能，长续航，适合通勤和运动',
                'uid': 1004,
                'productnum': 1,
                'category': 5,  # 数码电子
                'brand': '小米',
                'price': 299.0,
                'originalprice': 499.0,
                'totalprice': 299.0,
                'discount': 6.0,
                'province': '北京市',
                'city': '北京市',
                'citycode': '110100',
                'purchasechannels': '电商平台/线下门店',
                'producturl': 'https://example.com/product/456',
                'address': '朝阳区三里屯',
                'addresstitle': '小米之家三里屯店',
                'endtime': datetime.now() + timedelta(days=5),
                'status': 1
            },
            {
                'title': '美妆推荐-护肤套装',
                'content': '知名品牌护肤套装，包含水、乳、精华液，适合干性肌肤',
                'uid': 1005,
                'productnum': 1,
                'category': 6,  # 美妆护肤
                'brand': '欧莱雅',
                'price': 399.0,
                'originalprice': 699.0,
                'totalprice': 399.0,
                'discount': 5.7,
                'province': '广东省',
                'city': '深圳市',
                'citycode': '440300',
                'purchasechannels': '电商平台',
                'producturl': 'https://example.com/product/789',
                'endtime': datetime.now() + timedelta(days=20),
                'status': 0  # 待审核
            }
        ]
        
        added_count = 0
        for good_data in test_goods:
            goodpriceid = str(uuid.uuid4())
            good_price = GoodPrice(
                goodpriceid=goodpriceid,
                **good_data
            )
            db.session.add(good_price)
            added_count += 1
            
            # 为部分商品添加SKU (数码电子=5, 美妆护肤=6)
            if good_data['category'] in [5, 6]:
                # 添加2个不同规格的SKU
                sku1 = SkuStock(
                    skuid=str(uuid.uuid4()),
                    goodpriceid=goodpriceid,
                    skucode=f'SKU-{goodpriceid[:8]}-01',
                    price=good_data['price'],
                    stock=100,
                    specs='{"color": "黑色", "size": "标准版"}'
                )
                sku2 = SkuStock(
                    skuid=str(uuid.uuid4()),
                    goodpriceid=goodpriceid,
                    skucode=f'SKU-{goodpriceid[:8]}-02',
                    price=good_data['price'] + 50,
                    stock=50,
                    specs='{"color": "白色", "size": "豪华版"}'
                )
                db.session.add(sku1)
                db.session.add(sku2)
        
        db.session.commit()
        
        # 统计信息
        total = GoodPrice.query.count()
        by_status = {}
        for status in [0, 1, 2]:
            count = GoodPrice.query.filter_by(status=status).count()
            if count > 0:
                status_name = {0: '待审核', 1: '已通过', 2: '已拒绝'}[status]
                by_status[status_name] = count
        
        by_city = {}
        for citycode in ['440300', '110100']:
            count = GoodPrice.query.filter_by(citycode=citycode).count()
            if count > 0:
                city_name = {'440300': '深圳', '110100': '北京'}[citycode]
                by_city[city_name] = count
        
        print(f"✓ 成功添加 {added_count} 个测试商品!")
        print(f"\n数据统计:")
        print(f"  总商品数: {total}")
        print(f"  按状态分布: {by_status}")
        print(f"  按城市分布: {by_city}")
        
        # 显示部分商品信息
        print(f"\n部分商品列表:")
        goods = GoodPrice.query.limit(3).all()
        for good in goods:
            print(f"  • {good.title}")
            print(f"    ID: {good.goodpriceid}")
            print(f"    价格: ¥{good.price} (原价: ¥{good.originalprice})")
            print(f"    城市: {good.city}")
            print(f"    状态: {['待审核', '已通过', '已拒绝'][good.status]}")
            print()

if __name__ == '__main__':
    add_test_good_prices()

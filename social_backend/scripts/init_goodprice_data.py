"""
创建 GoodPrice 测试数据
"""
from api import db, create_app
from api.models.group_purchase import GoodPrice
from datetime import datetime, timedelta
import random
import uuid

def create_goodprice_test_data():
    """创建商品测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("创建 GoodPrice 测试数据")
        print("=" * 70)
        
        # 检查是否已有数据
        existing_count = GoodPrice.query.count()
        if existing_count > 0:
            print(f"\n📊 数据库中已有 {existing_count} 条商品数据")
            response = input("是否继续添加更多数据? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ 已取消")
                return
        
        # 测试商品数据
        test_products = [
            {
                "title": "iPhone 15 Pro Max 256GB 黑色钛金属",
                "content": "全新iPhone 15 Pro Max，配备A17 Pro芯片，钛金属边框，更轻更强。支持Action按钮，专业级相机系统。",
                "brand": "Apple",
                "category": 1,
                "price": 8999.00,
                "originalprice": 9999.00,
                "discount": 0.9,
                "province": "广东省",
                "city": "深圳市",
                "citycode": "440300",
                "purchasechannels": "京东自营",
            },
            {
                "title": "戴森V15 Detect无绳吸尘器",
                "content": "激光探测技术，科学量化清洁效果。强劲吸力，LCD屏幕实时显示。整屋深度清洁。",
                "brand": "Dyson",
                "category": 2,
                "price": 3990.00,
                "originalprice": 5490.00,
                "discount": 0.73,
                "province": "上海市",
                "city": "上海市",
                "citycode": "310000",
                "purchasechannels": "天猫旗舰店",
            },
            {
                "title": "小米14 Ultra 16GB+512GB 黑色",
                "content": "徕卡专业光学镜头，骁龙8 Gen3处理器，120Hz AMOLED屏幕，5000mAh电池+120W快充。",
                "brand": "小米",
                "category": 1,
                "price": 5499.00,
                "originalprice": 6499.00,
                "discount": 0.85,
                "province": "北京市",
                "city": "北京市",
                "citycode": "110000",
                "purchasechannels": "小米商城",
            },
            {
                "title": "海蓝之谜精华面霜60ml",
                "content": "经典修护面霜，深层滋润，改善肌肤纹理。适合干性及熟龄肌肤。",
                "brand": "La Mer",
                "category": 3,
                "price": 2380.00,
                "originalprice": 2650.00,
                "discount": 0.90,
                "province": "上海市",
                "city": "上海市",
                "citycode": "310000",
                "purchasechannels": "专柜",
            },
            {
                "title": "乐高建筑系列 巴黎埃菲尔铁塔",
                "content": "10307高难度成人积木，3428块颗粒，1:300比例还原。高度149cm，适合收藏展示。",
                "brand": "LEGO",
                "category": 4,
                "price": 4799.00,
                "originalprice": 5999.00,
                "discount": 0.80,
                "province": "江苏省",
                "city": "南京市",
                "citycode": "320100",
                "purchasechannels": "乐高官方旗舰店",
            },
            {
                "title": "耐克Air Jordan 1 Low 黑白熊猫配色",
                "content": "经典AJ1 Low设计，黑白熊猫配色百搭。真皮材质，舒适透气。男女同款。",
                "brand": "Nike",
                "category": 5,
                "price": 899.00,
                "originalprice": 1299.00,
                "discount": 0.69,
                "province": "浙江省",
                "city": "杭州市",
                "citycode": "330100",
                "purchasechannels": "Nike官网",
            },
            {
                "title": "雅诗兰黛小棕瓶精华50ml",
                "content": "明星修护精华，改善肌肤细纹、暗沉。适合各种肤质，早晚使用。",
                "brand": "Estée Lauder",
                "category": 3,
                "price": 890.00,
                "originalprice": 1080.00,
                "discount": 0.82,
                "province": "广东省",
                "city": "广州市",
                "citycode": "440100",
                "purchasechannels": "天猫国际",
            },
            {
                "title": "任天堂Switch OLED版游戏机",
                "content": "7英寸OLED屏幕，更鲜艳的色彩。64GB存储，增强音频，可调节支架。",
                "brand": "Nintendo",
                "category": 6,
                "price": 2498.00,
                "originalprice": 2599.00,
                "discount": 0.96,
                "province": "上海市",
                "city": "上海市",
                "citycode": "310000",
                "purchasechannels": "京东",
            },
            {
                "title": "索尼WH-1000XM5无线降噪耳机",
                "content": "业界领先的降噪技术，30小时续航，多点连接。轻量化设计，佩戴舒适。",
                "brand": "Sony",
                "category": 7,
                "price": 2299.00,
                "originalprice": 2799.00,
                "discount": 0.82,
                "province": "北京市",
                "city": "北京市",
                "citycode": "110000",
                "purchasechannels": "索尼官方商城",
            },
            {
                "title": "MacBook Air M3 13英寸 8GB+256GB",
                "content": "全新M3芯片，13.6英寸Liquid视网膜显示屏。轻薄便携，续航长达18小时。",
                "brand": "Apple",
                "category": 8,
                "price": 8999.00,
                "originalprice": 9999.00,
                "discount": 0.90,
                "province": "广东省",
                "city": "深圳市",
                "citycode": "440300",
                "purchasechannels": "Apple Store",
            },
            {
                "title": "优衣库男士圆领T恤 纯棉基础款",
                "content": "100%纯棉材质，柔软舒适。多色可选，百搭基础款。适合春夏季穿着。",
                "brand": "UNIQLO",
                "category": 9,
                "price": 39.00,
                "originalprice": 79.00,
                "discount": 0.49,
                "province": "江苏省",
                "city": "苏州市",
                "citycode": "320500",
                "purchasechannels": "优衣库官网",
            },
            {
                "title": "星巴克随行杯保温杯 473ml",
                "content": "304不锈钢内胆，真空保温。时尚设计，防漏密封。保温保冷两用。",
                "brand": "Starbucks",
                "category": 10,
                "price": 128.00,
                "originalprice": 199.00,
                "discount": 0.64,
                "province": "上海市",
                "city": "上海市",
                "citycode": "310000",
                "purchasechannels": "星巴克门店",
            },
        ]
        
        print(f"\n准备创建 {len(test_products)} 条商品数据...")
        print("-" * 70)
        
        created_count = 0
        
        for product in test_products:
            # 生成商品ID
            goodpriceid = str(uuid.uuid4())
            
            # 创建商品
            good_price = GoodPrice(
                goodpriceid=goodpriceid,
                uid=random.choice([1001, 1002, 1003, 1004, 1005]),
                title=product["title"],
                content=product["content"],
                brand=product["brand"],
                category=product["category"],
                price=product["price"],
                originalprice=product["originalprice"],
                discount=product["discount"],
                province=product["province"],
                city=product["city"],
                citycode=product["citycode"],
                purchasechannels=product["purchasechannels"],
                productnum=random.randint(10, 100),
                likenum=random.randint(50, 500),
                collectionnum=random.randint(20, 200),
                commentnum=0,  # 稍后添加评论
                viewnum=random.randint(100, 2000),
                status=1,  # 已通过审核
                createtime=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                updatetime=datetime.utcnow() - timedelta(days=random.randint(0, 10)),
                endtime=datetime.utcnow() + timedelta(days=random.randint(7, 30)),
            )
            
            db.session.add(good_price)
            created_count += 1
            print(f"✅ [{created_count}/{len(test_products)}] {product['title'][:50]}...")
        
        db.session.commit()
        
        print("\n" + "=" * 70)
        print(f"✅ 成功创建 {created_count} 条商品数据!")
        print("=" * 70)
        
        # 显示统计信息
        total_count = GoodPrice.query.count()
        print(f"\n📊 数据库统计:")
        print(f"   总商品数: {total_count}")
        
        # 显示一些样本
        print("\n📦 商品样本:")
        samples = GoodPrice.query.limit(3).all()
        for idx, gp in enumerate(samples, 1):
            print(f"\n  [{idx}] {gp.title}")
            print(f"      商品ID: {gp.goodpriceid}")
            print(f"      价格: ¥{gp.price} (原价: ¥{gp.originalprice})")
            print(f"      折扣: {gp.discount * 100:.0f}%")
            print(f"      品牌: {gp.brand}")
            print(f"      城市: {gp.city}")
        
        print("\n" + "=" * 70)
        print("💡 下一步:")
        print("   运行以下命令添加评论测试数据:")
        print("   python3 init_goodprice_comments.py")
        print("=" * 70)

if __name__ == '__main__':
    create_goodprice_test_data()

"""将 category 字段从 String 迁移到 Integer"""
from api import create_app, db
from sqlalchemy import text

def migrate_category_field():
    """迁移 category 字段数据类型"""
    app = create_app()
    
    with app.app_context():
        print("开始迁移 category 字段...")
        
        # 定义分类映射
        category_mapping = {
            '生鲜水果': 1,
            '餐饮美食': 2,
            '日用百货': 3,
            '运动户外': 4,
            '数码电子': 5,
            '美妆护肤': 6,
            '服装鞋包': 7,
            '家居家装': 8,
            '母婴用品': 9,
            '图书文娱': 10,
            '其他': 99
        }
        
        try:
            # 1. 创建临时列
            print("1. 创建临时列 category_int...")
            db.session.execute(text('ALTER TABLE good_prices ADD COLUMN category_int INTEGER'))
            db.session.commit()
            
            # 2. 迁移数据
            print("2. 迁移数据...")
            result = db.session.execute(text('SELECT goodpriceid, category FROM good_prices'))
            rows = result.fetchall()
            
            for row in rows:
                goodpriceid, category_str = row
                # 将字符串分类映射到整数
                category_int = category_mapping.get(category_str, 99)  # 默认为99(其他)
                
                db.session.execute(
                    text('UPDATE good_prices SET category_int = :cat WHERE goodpriceid = :id'),
                    {'cat': category_int, 'id': goodpriceid}
                )
                print(f"   • {goodpriceid}: '{category_str}' -> {category_int}")
            
            db.session.commit()
            
            # 3. 删除旧列
            print("3. 删除旧列 category...")
            db.session.execute(text('ALTER TABLE good_prices DROP COLUMN category'))
            db.session.commit()
            
            # 4. 重命名新列
            print("4. 重命名列 category_int -> category...")
            # SQLite 不支持直接重命名列，需要重建表
            db.session.execute(text('''
                CREATE TABLE good_prices_new (
                    goodpriceid VARCHAR(50) PRIMARY KEY,
                    uid INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content TEXT,
                    productnum INTEGER DEFAULT 1,
                    category INTEGER,
                    brand VARCHAR(100),
                    totalprice FLOAT,
                    price FLOAT NOT NULL,
                    originalprice FLOAT,
                    discount FLOAT,
                    createtime DATETIME,
                    updatetime DATETIME,
                    endtime DATETIME,
                    imgs TEXT,
                    pic VARCHAR(255),
                    province VARCHAR(100),
                    city VARCHAR(100),
                    citycode VARCHAR(20),
                    lat FLOAT,
                    lng FLOAT,
                    address VARCHAR(255),
                    addresstitle VARCHAR(255),
                    producturl VARCHAR(500),
                    purchasechannels VARCHAR(100),
                    likenum INTEGER DEFAULT 0,
                    unlikenum INTEGER DEFAULT 0,
                    collectionnum INTEGER DEFAULT 0,
                    commentnum INTEGER DEFAULT 0,
                    viewnum INTEGER DEFAULT 0,
                    status INTEGER DEFAULT 0,
                    statusmsg VARCHAR(255),
                    tag VARCHAR(50)
                )
            '''))
            
            # 复制数据
            db.session.execute(text('''
                INSERT INTO good_prices_new 
                SELECT goodpriceid, uid, title, content, productnum, category_int, brand,
                       totalprice, price, originalprice, discount, createtime, updatetime,
                       endtime, imgs, pic, province, city, citycode, lat, lng, address,
                       addresstitle, producturl, purchasechannels, likenum, unlikenum,
                       collectionnum, commentnum, viewnum, status, statusmsg, tag
                FROM good_prices
            '''))
            
            # 删除旧表
            db.session.execute(text('DROP TABLE good_prices'))
            
            # 重命名新表
            db.session.execute(text('ALTER TABLE good_prices_new RENAME TO good_prices'))
            
            db.session.commit()
            
            print("\n✓ 迁移完成!")
            print("\n分类映射表:")
            for name, code in sorted(category_mapping.items(), key=lambda x: x[1]):
                print(f"  {code}: {name}")
            
            # 验证数据
            print("\n验证数据:")
            result = db.session.execute(text('SELECT category, COUNT(*) as cnt FROM good_prices GROUP BY category'))
            for row in result:
                category_code, count = row
                category_name = [k for k, v in category_mapping.items() if v == category_code]
                category_name = category_name[0] if category_name else '未知'
                print(f"  分类 {category_code} ({category_name}): {count} 个商品")
                
        except Exception as e:
            print(f"\n✗ 迁移失败: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_category_field()

"""将 imgs 字段重命名为 albumpics"""
from api import create_app, db

def rename_imgs_to_albumpics():
    """将 imgs 字段重命名为 albumpics"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("重命名字段: imgs -> albumpics")
        print("=" * 60)
        
        try:
            # SQLite 不支持直接重命名列，需要重建表
            print("\n1. 创建新表结构...")
            db.session.execute(db.text('''
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
                    albumpics TEXT,
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
            
            print("2. 迁移数据 (imgs -> albumpics)...")
            # 复制数据，将 imgs 列映射到 albumpics
            db.session.execute(db.text('''
                INSERT INTO good_prices_new 
                SELECT goodpriceid, uid, title, content, productnum, category, brand,
                       totalprice, price, originalprice, discount, createtime, updatetime,
                       endtime, imgs, pic, province, city, citycode, lat, lng, address,
                       addresstitle, producturl, purchasechannels, likenum, unlikenum,
                       collectionnum, commentnum, viewnum, status, statusmsg, tag
                FROM good_prices
            '''))
            
            # 统计迁移的记录数
            result = db.session.execute(db.text('SELECT COUNT(*) FROM good_prices_new'))
            count = result.scalar()
            print(f"   ✓ 迁移了 {count} 条记录")
            
            print("3. 删除旧表...")
            db.session.execute(db.text('DROP TABLE good_prices'))
            
            print("4. 重命名新表...")
            db.session.execute(db.text('ALTER TABLE good_prices_new RENAME TO good_prices'))
            
            db.session.commit()
            
            print("\n5. 验证表结构:")
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('good_prices')
            
            has_albumpics = False
            has_imgs = False
            
            for col in columns:
                if col['name'] == 'albumpics':
                    has_albumpics = True
                    print(f"   ✓ 找到字段 'albumpics': {col['type']}")
                elif col['name'] == 'imgs':
                    has_imgs = True
                    print(f"   ! 仍存在旧字段 'imgs': {col['type']}")
            
            if has_albumpics and not has_imgs:
                print("\n✓ 字段重命名成功: imgs -> albumpics")
            else:
                print("\n✗ 字段重命名可能存在问题")
            
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"\n✗ 操作失败: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    rename_imgs_to_albumpics()

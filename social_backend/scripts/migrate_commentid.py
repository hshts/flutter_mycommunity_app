"""
更新 GoodPriceComment 的 commentid 从 String 改为 Integer
"""
from api import db, create_app
from api.models.group_purchase import GoodPriceComment, GoodPriceCommentReply, GoodPriceCommentLike

def migrate_commentid_to_integer():
    """迁移 commentid 从 String 到 Integer"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("迁移 GoodPriceComment.commentid 数据类型")
        print("从 String(50) 改为 Integer (自动增长)")
        print("=" * 60)
        
        # 由于 SQLite 不支持直接修改列类型,需要:
        # 1. 创建新表
        # 2. 迁移数据
        # 3. 删除旧表
        # 4. 重命名新表
        
        print("\n⚠️  警告: 此操作将删除所有现有评论数据!")
        print("   建议在测试环境中先测试此迁移")
        
        response = input("\n是否继续? (yes/no): ")
        
        if response.lower() != 'yes':
            print("❌ 迁移已取消")
            return
        
        try:
            # 删除旧数据
            print("\n1. 删除旧的评论数据...")
            GoodPriceCommentLike.query.delete()
            GoodPriceCommentReply.query.delete()
            GoodPriceComment.query.delete()
            db.session.commit()
            print("   ✅ 旧数据已删除")
            
            # 删除旧表
            print("\n2. 删除旧表结构...")
            db.session.execute(db.text('DROP TABLE IF EXISTS good_price_comment_likes'))
            db.session.execute(db.text('DROP TABLE IF EXISTS good_price_comment_replies'))
            db.session.execute(db.text('DROP TABLE IF EXISTS good_price_comments'))
            db.session.commit()
            print("   ✅ 旧表已删除")
            
            # 创建新表
            print("\n3. 创建新表结构...")
            db.create_all()
            print("   ✅ 新表已创建")
            
            print("\n" + "=" * 60)
            print("✅ 迁移完成!")
            print("=" * 60)
            print("\ncommentid 现在是 Integer 类型,会自动增长")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_commentid_to_integer()

from app import db
from datetime import datetime

class GoodPrice(db.Model):
    """好价商品模型"""
    __tablename__ = 'good_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='商品标题')
    desc = db.Column(db.Text, comment='商品描述')
    price = db.Column(db.Float, nullable=False, comment='价格')
    original_price = db.Column(db.Float, comment='原价')
    image_url = db.Column(db.String(500), comment='商品图片URL')
    
    # 平台信息
    platform = db.Column(db.String(50), comment='平台名称')
    platform_url = db.Column(db.String(500), comment='平台链接')
    
    # 分类和标签
    category = db.Column(db.String(100), comment='商品分类')
    tags = db.Column(db.Text, comment='标签，JSON格式存储')
    
    # 统计信息
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    comment_count = db.Column(db.Integer, default=0, comment='评论数')
    collect_count = db.Column(db.Integer, default=0, comment='收藏数')
    
    # 状态和时间
    status = db.Column(db.Integer, default=1, comment='状态: 1-正常, 0-下架')
    is_hot = db.Column(db.Boolean, default=False, comment='是否热门')
    is_recommend = db.Column(db.Boolean, default=False, comment='是否推荐')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 发布者信息
    user_id = db.Column(db.Integer, comment='发布者ID')
    user_name = db.Column(db.String(100), comment='发布者昵称')
    user_avatar = db.Column(db.String(500), comment='发布者头像')
    
    # 地理位置
    location = db.Column(db.String(200), comment='地理位置')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'price': self.price,
            'original_price': self.original_price,
            'imageUrl': self.image_url,
            'platform': self.platform,
            'platformUrl': self.platform_url,
            'category': self.category,
            'tags': self.tags,
            'viewCount': self.view_count,
            'likeCount': self.like_count,
            'commentCount': self.comment_count,
            'collectCount': self.collect_count,
            'status': self.status,
            'isHot': self.is_hot,
            'isRecommend': self.is_recommend,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'userId': self.user_id,
            'userName': self.user_name,
            'userAvatar': self.user_avatar,
            'location': self.location
        }
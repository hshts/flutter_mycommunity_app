from app import db
from datetime import datetime

class Collection(db.Model):
    """收藏模型"""
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    good_price_id = db.Column(db.Integer, nullable=False, comment='商品ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='收藏时间')
    
    # 添加联合唯一索引，防止重复收藏
    __table_args__ = (db.UniqueConstraint('user_id', 'good_price_id', name='uk_user_good'),)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'goodPriceId': self.good_price_id,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

class Like(db.Model):
    """点赞模型"""
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    target_id = db.Column(db.Integer, nullable=False, comment='目标ID')
    target_type = db.Column(db.Integer, nullable=False, comment='目标类型: 1-商品, 2-评论')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='点赞时间')
    
    # 添加联合唯一索引，防止重复点赞
    __table_args__ = (db.UniqueConstraint('user_id', 'target_id', 'target_type', name='uk_user_target'),)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'targetId': self.target_id,
            'targetType': self.target_type,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
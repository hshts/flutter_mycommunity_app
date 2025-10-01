from app import db
from datetime import datetime

class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, comment='评论内容')
    
    # 关联信息
    good_price_id = db.Column(db.Integer, nullable=False, comment='商品ID')
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    user_name = db.Column(db.String(100), comment='用户昵称')
    user_avatar = db.Column(db.String(500), comment='用户头像')
    
    # 回复相关
    parent_id = db.Column(db.Integer, comment='父评论ID，用于回复')
    reply_to_user_id = db.Column(db.Integer, comment='回复的用户ID')
    reply_to_user_name = db.Column(db.String(100), comment='回复的用户昵称')
    
    # 统计信息
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    reply_count = db.Column(db.Integer, default=0, comment='回复数')
    
    # 状态和时间
    status = db.Column(db.Integer, default=1, comment='状态: 1-正常, 0-删除')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'content': self.content,
            'goodPriceId': self.good_price_id,
            'userId': self.user_id,
            'userName': self.user_name,
            'userAvatar': self.user_avatar,
            'parentId': self.parent_id,
            'replyToUserId': self.reply_to_user_id,
            'replyToUserName': self.reply_to_user_name,
            'likeCount': self.like_count,
            'replyCount': self.reply_count,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
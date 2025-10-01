from app import db
from datetime import datetime

class Activity(db.Model):
    """活动模型"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='活动标题')
    desc = db.Column(db.Text, comment='活动描述')
    image_url = db.Column(db.String(500), comment='活动图片')
    
    # 活动类型和状态
    activity_type = db.Column(db.Integer, default=1, comment='活动类型: 1-团购, 2-秒杀, 3-优惠券')
    status = db.Column(db.Integer, default=1, comment='状态: 1-进行中, 2-已结束, 3-未开始')
    
    # 时间相关
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 参与相关
    min_people = db.Column(db.Integer, comment='最少参与人数')
    max_people = db.Column(db.Integer, comment='最多参与人数')
    current_people = db.Column(db.Integer, default=0, comment='当前参与人数')
    
    # 价格相关
    original_price = db.Column(db.Float, comment='原价')
    group_price = db.Column(db.Float, comment='团购价')
    
    # 创建者信息
    creator_id = db.Column(db.Integer, comment='创建者ID')
    creator_name = db.Column(db.String(100), comment='创建者昵称')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'imageUrl': self.image_url,
            'activityType': self.activity_type,
            'status': self.status,
            'startTime': self.start_time.isoformat() if self.start_time else None,
            'endTime': self.end_time.isoformat() if self.end_time else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'minPeople': self.min_people,
            'maxPeople': self.max_people,
            'currentPeople': self.current_people,
            'originalPrice': self.original_price,
            'groupPrice': self.group_price,
            'creatorId': self.creator_id,
            'creatorName': self.creator_name
        }
from app import db
from datetime import datetime

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, comment='用户名')
    nickname = db.Column(db.String(100), comment='昵称')
    email = db.Column(db.String(120), unique=True, comment='邮箱')
    phone = db.Column(db.String(20), unique=True, comment='手机号')
    password = db.Column(db.String(255), comment='密码hash')
    
    # 头像和个人信息
    avatar = db.Column(db.String(500), comment='头像URL')
    gender = db.Column(db.Integer, comment='性别: 1-男, 2-女, 0-未知')
    birthday = db.Column(db.Date, comment='生日')
    location = db.Column(db.String(200), comment='地理位置')
    
    # 状态和时间
    status = db.Column(db.Integer, default=1, comment='状态: 1-正常, 0-禁用')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'gender': self.gender,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'location': self.location,
            'status': self.status,
            'lastLogin': self.last_login.isoformat() if self.last_login else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
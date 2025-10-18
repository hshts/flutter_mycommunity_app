"""用户及相关关系模型"""
from api import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, default='新用户')
    password = db.Column(db.String(128))  # 存储加密后的密码（如MD5）
    mobile = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    sex = db.Column(db.String(5), default='0')  # 0未知 1男 2女
    birthday = db.Column(db.String(20))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    signature = db.Column(db.String(255))
    interest = db.Column(db.String(255))
    voice = db.Column(db.String(255))
    profilepicture = db.Column(db.String(255))
    usertype = db.Column(db.Integer, default=1)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 第三方绑定（占位字段）
    weixin_openid = db.Column(db.String(64))
    ios_userid = db.Column(db.String(128))
    alipay_userid = db.Column(db.String(128))

    def to_dict(self):
        return {
            'uid': self.uid,
            'username': self.username,
            'mobile': self.mobile,
            'email': self.email,
            'sex': self.sex,
            'birthday': self.birthday,
            'province': self.province,
            'city': self.city,
            'signature': self.signature,
            'interest': self.interest,
            'voice': self.voice,
            'profilepicture': self.profilepicture,
            'usertype': self.usertype,
        }


class UserVCode(db.Model):
    """验证码存储（用于手机/邮箱/按uid）"""
    __tablename__ = 'user_vcodes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, index=True)
    mobile = db.Column(db.String(32), index=True)
    email = db.Column(db.String(120), index=True)
    vcode = db.Column(db.String(10), nullable=False)
    token = db.Column(db.String(128))  # 用于邮箱登录预令牌
    expires_at = db.Column(db.DateTime)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    """关注关系"""
    __tablename__ = 'user_follow'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    followed = db.Column(db.Integer, nullable=False, index=True)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('uid', 'followed', name='uq_follow_uid_followed'),
    )


class Blacklist(db.Model):
    __tablename__ = 'user_blacklist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    blacklistuid = db.Column(db.Integer, nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint('uid', 'blacklistuid', name='uq_black_uid_user'),
    )


class NotInterested(db.Model):
    __tablename__ = 'user_notinteresteduids'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    notinteresteduid = db.Column(db.Integer, nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint('uid', 'notinteresteduid', name='uq_notinterest_uid_user'),
    )


class GoodPriceNotInterested(db.Model):
    __tablename__ = 'user_goodnotinteresteduids'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    goodpricenotinteresteduid = db.Column(db.Integer, nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint('uid', 'goodpricenotinteresteduid', name='uq_gp_notinterest_uid_user'),
    )


class PushDevice(db.Model):
    __tablename__ = 'user_push_devices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    brand = db.Column(db.String(50))
    pushtoken = db.Column(db.String(255))
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

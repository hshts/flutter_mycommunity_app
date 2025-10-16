from api import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    
    # 基本字段
    actid = db.Column(db.String(50), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1: 进行中, 2: 已结束
    peoplenum = db.Column(db.Integer)  # 活动总人数
    currentpeoplenum = db.Column(db.Integer, default=1)  # 当前参与人数
    startyear = db.Column(db.Integer)  # 开始时间戳
    endyear = db.Column(db.Integer)  # 结束时间戳
    
    # 位置信息
    address = db.Column(db.String(255))  # 活动地址
    addresstitle = db.Column(db.String(255))  # 地址标题
    lat = db.Column(db.Float)  # 纬度
    lng = db.Column(db.Float)  # 经度
    actcity = db.Column(db.String(100))  # 活动城市
    actprovince = db.Column(db.String(100))  # 活动省份
    
    # 图片信息
    coverimg = db.Column(db.String(255))  # 封面图片
    coverimgwh = db.Column(db.String(50))  # 封面图片宽高比
    actimagespath = db.Column(db.Text)  # 活动图片路径列表
    
    # 费用信息
    maxcost = db.Column(db.Float, default=0)  # 最大费用
    mincost = db.Column(db.Float, default=0)  # 最小费用
    paytype = db.Column(db.Integer, default=0)  # 支付类型 0: 免费 1: 后付款 2: 先付款
    
    # 关联信息
    uid = db.Column(db.Integer, nullable=False)  # 发起人用户ID
    goodpriceid = db.Column(db.String(50))  # 关联商品ID
    
    # 统计信息
    likenum = db.Column(db.Integer, default=0)  # 点赞数
    collectionnum = db.Column(db.Integer, default=0)  # 收藏数
    commentnum = db.Column(db.Integer, default=0)  # 评论数
    viewnum = db.Column(db.Integer, default=0)  # 浏览数
    joinnum = db.Column(db.Integer, default=0)  # 参与数
    
    # 状态字段
    locked = db.Column(db.Integer, default=0)  # 是否锁定(活动开始)
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'actid': self.actid,
            'content': self.content,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'updatetime': self.updatetime.isoformat() if self.updatetime else None,
            'status': self.status,
            'peoplenum': self.peoplenum,
            'currentpeoplenum': self.currentpeoplenum,
            'startyear': self.startyear,
            'endyear': self.endyear,
            'address': self.address,
            'addresstitle': self.addresstitle,
            'lat': self.lat,
            'lng': self.lng,
            'actcity': self.actcity,
            'actprovince': self.actprovince,
            'coverimg': self.coverimg,
            'coverimgwh': self.coverimgwh,
            'actimagespath': self.actimagespath,
            'maxcost': self.maxcost,
            'mincost': self.mincost,
            'paytype': self.paytype,
            'uid': self.uid,
            'goodpriceid': self.goodpriceid,
            'likenum': self.likenum,
            'collectionnum': self.collectionnum,
            'commentnum': self.commentnum,
            'viewnum': self.viewnum,
            'joinnum': self.joinnum,
            'locked': self.locked
        }
    
    def __repr__(self):
        return f'<Activity {self.actid}>'
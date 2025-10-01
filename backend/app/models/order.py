from app import db
from datetime import datetime

class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment='下单用户ID')
    activity_id = db.Column(db.Integer, nullable=False, comment='团购活动ID')
    good_price_id = db.Column(db.Integer, nullable=True, comment='商品ID')
    order_no = db.Column(db.String(64), unique=True, nullable=False, comment='订单号')
    amount = db.Column(db.Float, nullable=False, comment='订单金额')
    status = db.Column(db.Integer, default=0, comment='订单状态: 0-待支付, 1-已支付, 2-已取消, 3-已完成')
    pay_time = db.Column(db.DateTime, comment='支付时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'activityId': self.activity_id,
            'goodPriceId': self.good_price_id,
            'orderNo': self.order_no,
            'amount': self.amount,
            'status': self.status,
            'payTime': self.pay_time.isoformat() if self.pay_time else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

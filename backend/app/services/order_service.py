from app import db
from app.models.order import Order
from app.models.activity import Activity
from app.models.user import User
from app.utils.response import success_response, error_response
from datetime import datetime
import uuid

class OrderService:
    """订单业务逻辑"""
    @staticmethod
    def create_order(user_id, activity_id, good_price_id, amount):
        try:
            user = User.query.get(user_id)
            activity = Activity.query.get(activity_id)
            if not user or not activity:
                return None, "用户或活动不存在"
            order_no = str(uuid.uuid4()).replace('-', '')[:20]
            order = Order(
                user_id=user_id,
                activity_id=activity_id,
                good_price_id=good_price_id,
                order_no=order_no,
                amount=amount,
                status=0,
                created_at=datetime.utcnow()
            )
            db.session.add(order)
            db.session.commit()
            return order.to_dict(), "订单创建成功"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def pay_order(order_id):
        try:
            order = Order.query.get(order_id)
            if not order:
                return False, "订单不存在"
            order.status = 1
            order.pay_time = datetime.utcnow()
            db.session.commit()
            return True, "支付成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_order_list(user_id, status=None):
        try:
            query = Order.query.filter_by(user_id=user_id)
            if status is not None:
                query = query.filter_by(status=status)
            orders = query.order_by(Order.created_at.desc()).all()
            return [o.to_dict() for o in orders], "获取成功"
        except Exception as e:
            return [], str(e)

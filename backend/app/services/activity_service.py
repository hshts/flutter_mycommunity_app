from flask import request
from app import db
from app.models.activity import Activity
from app.models.user import User
from app.utils.response import success_response, error_response
from datetime import datetime

class ActivityService:
    """团购活动业务逻辑"""
    @staticmethod
    def create_activity(title, desc, image_url, activity_type, start_time, end_time, min_people, max_people, original_price, group_price, creator_id):
        try:
            creator = User.query.get(creator_id)
            if not creator:
                return None, "创建者不存在"
            activity = Activity(
                title=title,
                desc=desc,
                image_url=image_url,
                activity_type=activity_type,
                start_time=start_time,
                end_time=end_time,
                min_people=min_people,
                max_people=max_people,
                original_price=original_price,
                group_price=group_price,
                creator_id=creator_id,
                creator_name=creator.nickname or creator.username,
                status=1,
                created_at=datetime.utcnow()
            )
            db.session.add(activity)
            db.session.commit()
            return activity.to_dict(), "活动创建成功"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def join_activity(activity_id, user_id, username, sex):
        try:
            activity = Activity.query.get(activity_id)
            if not activity:
                return None, "活动不存在"
            if activity.status != 1:
                return None, "活动已结束或未开始"
            # 这里可以添加参与人数限制逻辑
            activity.current_people += 1
            db.session.commit()
            return activity.to_dict(), "参与成功"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_activity_list(good_price_id=None):
        try:
            query = Activity.query.filter(Activity.status == 1)
            # 可根据商品ID筛选活动
            # if good_price_id:
            #     query = query.filter(Activity.good_price_id == good_price_id)
            activities = query.order_by(Activity.start_time.desc()).all()
            return [a.to_dict() for a in activities], "获取成功"
        except Exception as e:
            return [], str(e)

    @staticmethod
    def client_pay_success(order_id, user_id):
        # 这里只做演示，实际应有订单模型
        return True, "支付成功"
from flask import Blueprint, request
from app.services.activity_service import ActivityService
from app.utils.response import success_response, error_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('activity', __name__)

@bp.route('/create', methods=['POST'])
@auth_required
def create():
    """创建团购活动"""
    data = request.form or request.json or {}
    title = data.get('title')
    desc = data.get('desc')
    image_url = data.get('image_url')
    activity_type = int(data.get('activity_type', 1))
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    min_people = int(data.get('min_people', 2))
    max_people = int(data.get('max_people', 10))
    original_price = float(data.get('original_price', 0))
    group_price = float(data.get('group_price', 0))
    creator_id = int(data.get('creator_id', get_current_user_id()))
    activity, msg = ActivityService.create_activity(title, desc, image_url, activity_type, start_time, end_time, min_people, max_people, original_price, group_price, creator_id)
    if activity:
        return success_response(data=activity, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/join', methods=['POST'])
@auth_required
def join():
    """参与团购活动"""
    activity_id = int(request.form.get('actid'))
    user_id = int(request.form.get('uid', get_current_user_id()))
    username = request.form.get('username')
    sex = request.form.get('sex')
    activity, msg = ActivityService.join_activity(activity_id, user_id, username, sex)
    if activity:
        return success_response(data=activity, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/list', methods=['GET'])
def list_activities():
    """获取活动列表"""
    good_price_id = request.args.get('goodpriceid')
    activities, msg = ActivityService.get_activity_list(good_price_id)
    return success_response(data=activities, message=msg)

@bp.route('/clientPaySuccess', methods=['POST'])
@auth_required
def client_pay_success():
    """客户端支付成功通知"""
    order_id = request.form.get('orderid')
    user_id = int(request.form.get('uid', get_current_user_id()))
    success, msg = ActivityService.client_pay_success(order_id, user_id)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

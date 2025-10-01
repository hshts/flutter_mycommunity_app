from flask import Blueprint, request
from app.services.order_service import OrderService
from app.utils.response import success_response, error_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('order', __name__)

@bp.route('/create', methods=['POST'])
@auth_required
def create():
    user_id = int(request.form.get('uid', get_current_user_id()))
    activity_id = int(request.form.get('activity_id'))
    good_price_id = request.form.get('good_price_id')
    amount = float(request.form.get('amount', 0))
    order, msg = OrderService.create_order(user_id, activity_id, good_price_id, amount)
    if order:
        return success_response(data=order, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/pay', methods=['POST'])
@auth_required
def pay():
    order_id = int(request.form.get('order_id'))
    success, msg = OrderService.pay_order(order_id)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/list', methods=['GET'])
@auth_required
def list_orders():
    user_id = int(request.args.get('uid', get_current_user_id()))
    status = request.args.get('status')
    status = int(status) if status is not None else None
    orders, msg = OrderService.get_order_list(user_id, status)
    return success_response(data=orders, message=msg)

from flask import Blueprint, request
from app.services.push_service import PushService
from app.utils.response import success_response, error_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('push', __name__)

@bp.route('/message', methods=['POST'])
@auth_required
def push_message():
    user_id = int(request.form.get('uid', get_current_user_id()))
    title = request.form.get('title')
    content = request.form.get('content')
    msg_type = request.form.get('msg_type', 'system')
    data, msg = PushService.push_message(user_id, title, content, msg_type)
    if data:
        return success_response(data=data, message=msg)
    else:
        return error_response(message=msg)

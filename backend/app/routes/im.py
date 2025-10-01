from flask import Blueprint, request
from app.services.im_service import IMService
from app.utils.response import success_response, error_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('im', __name__)

@bp.route('/send', methods=['POST'])
@auth_required
def send():
    sender_id = int(request.form.get('sender_id', get_current_user_id()))
    receiver_id = int(request.form.get('receiver_id'))
    content = request.form.get('content')
    msg_type = request.form.get('msg_type', 'text')
    msg, msg_text = IMService.send_message(sender_id, receiver_id, content, msg_type)
    return success_response(data=msg, message=msg_text)

@bp.route('/conversation_list', methods=['GET'])
@auth_required
def conversation_list():
    user_id = int(request.args.get('uid', get_current_user_id()))
    convs, msg = IMService.get_conversation_list(user_id)
    return success_response(data=convs, message=msg)

@bp.route('/unread_count', methods=['GET'])
@auth_required
def unread_count():
    user_id = int(request.args.get('uid', get_current_user_id()))
    count, msg = IMService.get_unread_count(user_id)
    return success_response(data={"unread_count": count}, message=msg)

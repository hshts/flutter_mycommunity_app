from flask import Blueprint, request
from app.services.aliyun_service import AliyunService
from app.utils.response import success_response, error_response

bp = Blueprint('aliyun', __name__)

@bp.route('/send_sms', methods=['POST'])
def send_sms():
    phone = request.form.get('phone')
    code = request.form.get('code')
    success, msg = AliyunService.send_sms(phone, code)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')
    code = request.form.get('code')
    success, msg = AliyunService.send_email(email, code)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/upload_oss', methods=['POST'])
def upload_oss():
    file = request.files.get('file')
    data, msg = AliyunService.upload_oss(file)
    return success_response(data=data, message=msg)

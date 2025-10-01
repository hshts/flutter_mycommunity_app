from flask import Blueprint, request
from app.services.upload_service import UploadService
from app.utils.response import success_response, error_response

bp = Blueprint('upload', __name__)

@bp.route('/image', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    data, msg = UploadService.upload_image(file)
    if data:
        return success_response(data=data, message=msg)
    else:
        return error_response(message=msg)

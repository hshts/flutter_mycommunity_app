import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.response import success_response, error_response
from datetime import datetime

class UploadService:
    """图片上传服务"""
    @staticmethod
    def upload_image(file):
        if not file:
            return None, "未选择文件"
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            return None, "不支持的图片格式"
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads/')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        save_name = datetime.now().strftime('%Y%m%d%H%M%S_') + filename
        save_path = os.path.join(upload_folder, save_name)
        file.save(save_path)
        url = f'/uploads/{save_name}'
        return {'url': url}, "上传成功"
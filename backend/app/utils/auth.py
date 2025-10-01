from functools import wraps
from flask import request, jsonify

def auth_required(f):
    """简单的认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 这里可以添加JWT或其他认证逻辑
        # 暂时只检查是否有Authorization头部
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                "code": 401,
                "message": "未提供认证信息",
                "success": False
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """获取当前用户ID"""
    # 这里应该从JWT token中解析用户ID
    # 暂时返回固定值用于测试
    return 1
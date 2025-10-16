from functools import wraps
from flask import request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def token_required(f):
    """
    装饰器：验证JWT token
    在测试环境中会跳过验证
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 在测试环境中跳过token验证
        if current_app.config.get('TESTING'):
            return f(*args, **kwargs)
            
        try:
            # 验证JWT token
            verify_jwt_in_request()
            # 获取用户ID
            current_user_id = get_jwt_identity()
            # 可以将用户ID添加到请求上下文中供后续使用
            request.current_user_id = current_user_id
        except Exception as e:
            return {'error': 'Token is missing or invalid'}, 401
        return f(*args, **kwargs)
    return decorated_function
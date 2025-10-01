from flask import Blueprint, request
from app.services.user_service import UserService
from app.utils.response import success_response, error_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('user', __name__)

# 通用 OPTIONS 响应，解决 CORS 预检 403
@bp.route('/<path:path>', methods=['OPTIONS'])
def user_options(path):
    from flask import make_response, request
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers', 'Authorization,Content-Type')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.status_code = 200
    return response

@bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.form or request.json or {}
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    nickname = data.get('nickname')
    user, msg = UserService.register_user(username, email, phone, password, nickname)
    if user:
        return success_response(data=user, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.form or request.json or {}
    login_type = data.get('login_type')
    identifier = data.get('identifier')
    password = data.get('password')
    verification_code = data.get('verification_code')
    user, msg = UserService.login_user(login_type, identifier, password, verification_code)
    if user:
        return success_response(data=user, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/info', methods=['GET'])
@auth_required
def info():
    """获取用户信息"""
    user_id = request.args.get('uid') or get_current_user_id()
    user, msg = UserService.get_user_info(int(user_id))
    if user:
        return success_response(data=user, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/update', methods=['POST'])
@auth_required
def update():
    """更新用户信息"""
    user_id = request.form.get('uid') or get_current_user_id()
    kwargs = {
        'nickname': request.form.get('nickname'),
        'avatar': request.form.get('avatar'),
        'gender': request.form.get('gender'),
        'birthday': request.form.get('birthday'),
        'location': request.form.get('location')
    }
    user, msg = UserService.update_user_info(int(user_id), **kwargs)
    if user:
        return success_response(data=user, message=msg)
    else:
        return error_response(message=msg)

@bp.route('/change_password', methods=['POST'])
@auth_required
def change_password():
    """修改密码"""
    user_id = request.form.get('uid') or get_current_user_id()
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    success, msg = UserService.change_password(int(user_id), old_password, new_password)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    """发送验证码"""
    contact = request.form.get('contact')
    contact_type = request.form.get('contact_type')
    success, msg = UserService.send_verification_code(contact, contact_type)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/reset_password', methods=['POST'])
def reset_password():
    """重置密码"""
    contact = request.form.get('contact')
    contact_type = request.form.get('contact_type')
    verification_code = request.form.get('verification_code')
    new_password = request.form.get('new_password')
    success, msg = UserService.reset_password(contact, contact_type, verification_code, new_password)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

@bp.route('/list', methods=['GET'])
@auth_required
def user_list():
    """获取用户列表（管理员功能）"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search_keyword = request.args.get('search', '')
    users, total, msg = UserService.get_user_list(page, per_page, search_keyword)
    return success_response(data={"items": users, "total": total}, message=msg)

@bp.route('/update_status', methods=['POST'])
@auth_required
def update_status():
    """更新用户状态（管理员功能）"""
    user_id = request.form.get('uid')
    status = int(request.form.get('status', 1))
    success, msg = UserService.update_user_status(int(user_id), status)
    if success:
        return success_response(message=msg)
    else:
        return error_response(message=msg)

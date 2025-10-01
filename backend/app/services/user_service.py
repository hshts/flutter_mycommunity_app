from flask import request
from app import db
from app.models.user import User
from app.utils.response import success_response, error_response
from sqlalchemy import or_
from datetime import datetime, timedelta
import hashlib
import jwt
import re
import random
import string

class UserService:
    """用户服务业务逻辑"""
    
    SECRET_KEY = "your-secret-key-change-in-production"
    
    @staticmethod
    def generate_token(user_id, expires_in=7*24*3600):
        """生成JWT token"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=expires_in),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, UserService.SECRET_KEY, algorithm='HS256')
            return token
        except Exception as e:
            return None
    
    @staticmethod
    def verify_token(token):
        """验证JWT token"""
        try:
            payload = jwt.decode(token, UserService.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def hash_password(password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        """验证密码"""
        return UserService.hash_password(password) == hashed_password
    
    @staticmethod
    def validate_email(email):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def generate_verification_code():
        """生成验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def register_user(username=None, email=None, phone=None, password=None, nickname=None):
        """用户注册"""
        try:
            # 参数验证
            if not any([username, email, phone]):
                return None, "用户名、邮箱或手机号至少提供一个"
            
            if not password:
                return None, "密码不能为空"
            
            if len(password) < 6:
                return None, "密码长度至少6位"
            
            # 邮箱格式验证
            if email and not UserService.validate_email(email):
                return None, "邮箱格式不正确"
            
            # 手机号格式验证
            if phone and not UserService.validate_phone(phone):
                return None, "手机号格式不正确"
            
            # 检查用户是否已存在
            existing_conditions = []
            if username:
                existing_conditions.append(User.username == username)
            if email:
                existing_conditions.append(User.email == email)
            if phone:
                existing_conditions.append(User.phone == phone)
            
            existing_user = User.query.filter(or_(*existing_conditions)).first()
            if existing_user:
                if existing_user.username == username:
                    return None, "用户名已存在"
                elif existing_user.email == email:
                    return None, "邮箱已被注册"
                elif existing_user.phone == phone:
                    return None, "手机号已被注册"
            
            # 创建新用户
            user = User(
                username=username,
                email=email,
                phone=phone,
                nickname=nickname or username,
                password=UserService.hash_password(password),
                status=1
            )
            
            db.session.add(user)
            db.session.commit()
            
            # 生成token
            token = UserService.generate_token(user.id)
            
            user_dict = user.to_dict()
            user_dict['token'] = token
            
            return user_dict, "注册成功"
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def login_user(login_type, identifier, password=None, verification_code=None):
        """用户登录"""
        try:
            # 根据登录类型查找用户
            if login_type == "phone_password":
                if not UserService.validate_phone(identifier):
                    return None, "手机号格式不正确"
                user = User.query.filter_by(phone=identifier).first()
            elif login_type == "phone_sms":
                if not UserService.validate_phone(identifier):
                    return None, "手机号格式不正确"
                user = User.query.filter_by(phone=identifier).first()
            elif login_type == "email_password":
                if not UserService.validate_email(identifier):
                    return None, "邮箱格式不正确"
                user = User.query.filter_by(email=identifier).first()
            elif login_type == "email_sms":
                if not UserService.validate_email(identifier):
                    return None, "邮箱格式不正确"
                user = User.query.filter_by(email=identifier).first()
            else:
                return None, "不支持的登录方式"
            
            if not user:
                return None, "用户不存在"
            
            if user.status != 1:
                return None, "用户已被禁用"
            
            # 验证密码或验证码
            if login_type in ["phone_password", "email_password"]:
                if not password:
                    return None, "密码不能为空"
                if not UserService.verify_password(password, user.password):
                    return None, "密码错误"
            elif login_type in ["phone_sms", "email_sms"]:
                if not verification_code:
                    return None, "验证码不能为空"
                # 这里应该验证短信或邮箱验证码，暂时简化处理
                if verification_code != "123456":  # 模拟验证码
                    return None, "验证码错误"
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # 生成token
            token = UserService.generate_token(user.id)
            
            user_dict = user.to_dict()
            user_dict['token'] = token
            
            return user_dict, "登录成功"
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_user_info(user_id):
        """获取用户信息"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "用户不存在"
            
            if user.status != 1:
                return None, "用户已被禁用"
            
            return user.to_dict(), "获取成功"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_user_info(user_id, **kwargs):
        """更新用户信息"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "用户不存在"
            
            # 可更新的字段
            updatable_fields = ['nickname', 'avatar', 'gender', 'birthday', 'location']
            
            updated = False
            for field in updatable_fields:
                if field in kwargs and kwargs[field] is not None:
                    setattr(user, field, kwargs[field])
                    updated = True
            
            if updated:
                user.updated_at = datetime.utcnow()
                db.session.commit()
                return user.to_dict(), "更新成功"
            else:
                return user.to_dict(), "没有更新任何信息"
                
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """修改密码"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "用户不存在"
            
            # 验证旧密码
            if not UserService.verify_password(old_password, user.password):
                return False, "原密码错误"
            
            # 验证新密码
            if len(new_password) < 6:
                return False, "新密码长度至少6位"
            
            # 更新密码
            user.password = UserService.hash_password(new_password)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            return True, "密码修改成功"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def send_verification_code(contact, contact_type):
        """发送验证码"""
        try:
            # 验证联系方式格式
            if contact_type == "phone":
                if not UserService.validate_phone(contact):
                    return False, "手机号格式不正确"
            elif contact_type == "email":
                if not UserService.validate_email(contact):
                    return False, "邮箱格式不正确"
            else:
                return False, "不支持的联系方式类型"
            
            # 生成验证码
            code = UserService.generate_verification_code()
            
            # 这里应该调用短信或邮件服务发送验证码
            # 暂时模拟发送成功，实际项目中需要集成短信和邮件服务
            print(f"验证码发送到 {contact}: {code}")
            
            # 实际项目中应该将验证码存储到缓存(Redis)中，设置过期时间
            # 这里暂时返回成功
            
            return True, "验证码发送成功"
            
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def reset_password(contact, contact_type, verification_code, new_password):
        """重置密码"""
        try:
            # 验证联系方式格式
            if contact_type == "phone":
                if not UserService.validate_phone(contact):
                    return False, "手机号格式不正确"
                user = User.query.filter_by(phone=contact).first()
            elif contact_type == "email":
                if not UserService.validate_email(contact):
                    return False, "邮箱格式不正确"
                user = User.query.filter_by(email=contact).first()
            else:
                return False, "不支持的联系方式类型"
            
            if not user:
                return False, "用户不存在"
            
            # 验证验证码（这里简化处理）
            if verification_code != "123456":
                return False, "验证码错误"
            
            # 验证新密码
            if len(new_password) < 6:
                return False, "密码长度至少6位"
            
            # 更新密码
            user.password = UserService.hash_password(new_password)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            return True, "密码重置成功"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_user_list(page=1, per_page=20, search_keyword=""):
        """获取用户列表（管理员功能）"""
        try:
            query = User.query
            
            # 搜索功能
            if search_keyword:
                query = query.filter(
                    or_(
                        User.username.like(f'%{search_keyword}%'),
                        User.nickname.like(f'%{search_keyword}%'),
                        User.email.like(f'%{search_keyword}%'),
                        User.phone.like(f'%{search_keyword}%')
                    )
                )
            
            # 分页
            total = query.count()
            offset = (page - 1) * per_page
            users = query.offset(offset).limit(per_page).all()
            
            user_list = [user.to_dict() for user in users]
            
            return user_list, total, "获取成功"
            
        except Exception as e:
            return [], 0, str(e)
    
    @staticmethod
    def update_user_status(user_id, status):
        """更新用户状态（管理员功能）"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "用户不存在"
            
            if status not in [0, 1]:
                return False, "状态值无效"
            
            user.status = status
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            status_text = "启用" if status == 1 else "禁用"
            return True, f"用户{status_text}成功"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
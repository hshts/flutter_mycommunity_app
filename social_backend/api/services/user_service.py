from datetime import datetime, timedelta
import hashlib
import random
import string

from api import db
from api.models import User, UserVCode, Follow, Blacklist, NotInterested, GoodPriceNotInterested, PushDevice


def _md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class UserService:
    @staticmethod
    def login(mobile: str = None, email: str = None, password: str = None):
        if not any([mobile, email]):
            raise ValueError('mobile or email required')
        q = User.query
        if mobile:
            q = q.filter_by(mobile=mobile)
        if email:
            q = q.filter_by(email=email)
        user = q.first()
        if not user:
            # 注册一个账号（简化）
            user = User(mobile=mobile, email=email, username=(email or mobile or '新用户'))
            if password:
                user.password = password
            db.session.add(user)
            db.session.commit()
        else:
            # 校验密码（如果提供）
            if password and user.password and user.password != password:
                raise ValueError('invalid credentials')
        return user

    @staticmethod
    def send_mobile_otp(mobile: str) -> bool:
        code = ''.join(random.choices(string.digits, k=6))
        v = UserVCode(mobile=mobile, vcode=code, expires_at=datetime.utcnow() + timedelta(minutes=10))
        db.session.add(v)
        db.session.commit()
        return True

    @staticmethod
    def email_code_login(email: str):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        code = ''.join(random.choices(string.digits, k=6))
        v = UserVCode(email=email, vcode=code, token=token, expires_at=datetime.utcnow() + timedelta(minutes=15))
        db.session.add(v)
        db.session.commit()
        return token

    @staticmethod
    def login_mobile(mobile: str, vcode: str, country: str = None):
        now = datetime.utcnow()
        v = UserVCode.query.filter_by(mobile=mobile, vcode=vcode).order_by(UserVCode.id.desc()).first()
        if not v or (v.expires_at and v.expires_at < now):
            raise ValueError('invalid vcode')
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            user = User(mobile=mobile, username=f'用户{mobile[-4:]}')
            db.session.add(user)
            db.session.commit()
        return user

    @staticmethod
    def email_code_login_validity(email: str, code: str, token: str):
        now = datetime.utcnow()
        v = UserVCode.query.filter_by(email=email, vcode=code, token=token).order_by(UserVCode.id.desc()).first()
        if not v or (v.expires_at and v.expires_at < now):
            raise ValueError('invalid code or token')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, username=email.split('@')[0])
            db.session.add(user)
            db.session.commit()
        return user

    @staticmethod
    def update_push_token(uid: int, brand: str, pushtoken: str) -> bool:
        d = PushDevice.query.filter_by(uid=uid).first()
        if not d:
            d = PushDevice(uid=uid)
            db.session.add(d)
        d.brand = brand
        d.pushtoken = pushtoken
        db.session.commit()
        return True

    @staticmethod
    def update_mobile(uid: int, vcode: str, mobile: str, country: str = None, confirm: int = 0):
        # 简化校验
        now = datetime.utcnow()
        v = UserVCode.query.filter_by(mobile=mobile, vcode=vcode).order_by(UserVCode.id.desc()).first()
        if not v or (v.expires_at and v.expires_at < now):
            raise ValueError('invalid vcode')
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.mobile = mobile
        db.session.commit()
        return user

    @staticmethod
    def get_profile_by_uid(uid: int):
        # 
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        return user if user else {}

    @staticmethod
    def update_avatar_file(uid: int, imagefile) -> bool:
        # 这里不真正保存文件，示意更新头像URL
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.profilepicture = f'/static/avatars/{uid}.png'
        db.session.commit()
        return True

    @staticmethod
    def update_avatar_url(uid: int, avatar_url: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.profilepicture = avatar_url
        db.session.commit()
        return True

    @staticmethod
    def update_sex(uid: int, sex: string) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.sex = sex
        db.session.commit()
        return True

    @staticmethod
    def update_subject(uid: int, subject: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        # 简化：直接写到interest
        user.interest = subject
        db.session.commit()
        return True

    @staticmethod
    def update_birthday(uid: int, birthday: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.birthday = birthday
        db.session.commit()
        return True

    @staticmethod
    def update_name(uid: int, name: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.username = name
        db.session.commit()
        return True

    @staticmethod
    def update_location(uid: int, province: str, city: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.province = province
        user.city = city
        db.session.commit()
        return True

    @staticmethod
    def update_signature(uid: int, signature: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.signature = signature
        db.session.commit()
        return True

    @staticmethod
    def update_password(token: str, uid: int, new_password: str, repeat_new_password: str) -> bool:
        if new_password != repeat_new_password:
            raise ValueError('password mismatch')
        print(uid)
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.password = new_password
        db.session.commit()
        return True

    @staticmethod
    def update_interest(uid: int, interest: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.interest = interest
        db.session.commit()
        return True

    @staticmethod
    def update_voice(uid: int, voice: str) -> bool:
        user = User.query.get(uid)
        if not user:
            raise ValueError('user not found')
        user.voice = voice
        db.session.commit()
        return True

    @staticmethod
    def deltoken(token: str, uid: int) -> bool:
        # 演示：无状态，直接返回成功
        return True

    @staticmethod
    def update_notinterested_uids(uid: int, ids: list[int]) -> bool:
        for i in ids:
            exist = NotInterested.query.filter_by(uid=uid, notinteresteduid=i).first()
            if not exist:
                db.session.add(NotInterested(uid=uid, notinteresteduid=i))
        db.session.commit()
        return True

    @staticmethod
    def goodprice_notinterested_uids(uid: int, ids: list[int]) -> bool:
        for i in ids:
            exist = GoodPriceNotInterested.query.filter_by(uid=uid, goodpricenotinteresteduid=i).first()
            if not exist:
                db.session.add(GoodPriceNotInterested(uid=uid, goodpricenotinteresteduid=i))
        db.session.commit()
        return True

    @staticmethod
    def update_blacklist(uid: int, ids: list[int]) -> bool:
        for i in ids:
            exist = Blacklist.query.filter_by(uid=uid, blacklistuid=i).first()
            if not exist:
                db.session.add(Blacklist(uid=uid, blacklistuid=i))
        db.session.commit()
        return True

    @staticmethod
    def get_follow(uid: int) -> list[int]:
        return [f.followed for f in Follow.query.filter_by(uid=uid).all()]

    @staticmethod
    def sel_follower_user(uid: int, followed: int):
        f = Follow.query.filter_by(uid=uid, followed=followed).first()
        return f.createtime.isoformat() if f else None

    @staticmethod
    def follow(uid: int, followed: int, is_clean: bool = False) -> bool:
        f = Follow.query.filter_by(uid=uid, followed=followed).first()
        if is_clean:
            if f:
                db.session.delete(f)
                db.session.commit()
            return True
        if not f:
            db.session.add(Follow(uid=uid, followed=followed))
            db.session.commit()
        return True

    @staticmethod
    def get_userinfo(uid: int):
        u = User.query.get(uid)
        return u.to_dict() if u else None

    # ===== 扩展：关注/粉丝/用户列表 =====
    @staticmethod
    def get_users_by_ids(ids: list[int]):
        if not ids:
            return []
        users = User.query.filter(User.uid.in_(ids)).all()
        by_id = {u.uid: u for u in users}
        result = []
        for i in ids:
            u = by_id.get(i)
            if not u:
                u = User(uid=i, username=f'用户{i}')
                db.session.add(u)
                db.session.flush()
            result.append(u)
        db.session.commit()
        return [u.to_dict() for u in result]

    @staticmethod
    def get_follow_users(uid: int, current_index: int = 0, page_size: int = 20):
        q = Follow.query.filter_by(uid=uid).order_by(Follow.createtime.desc())
        items = q.offset(current_index).limit(page_size).all()
        ids = [i.followed for i in items]
        return UserService.get_users_by_ids(ids)

    @staticmethod
    def get_fans_users(uid: int, current_index: int = 0, page_size: int = 20):
        q = Follow.query.filter_by(followed=uid).order_by(Follow.createtime.desc())
        items = q.offset(current_index).limit(page_size).all()
        ids = [i.uid for i in items]
        return UserService.get_users_by_ids(ids)

    @staticmethod
    def get_single_conversation(uid: int, touid: int, timeline_id: str | None):
        tid = timeline_id or f'single_{min(uid, touid)}_{max(uid, touid)}'
        return {
            'timeline_id': tid,
            'uid': uid,
            'touid': touid,
            'name': '私聊',
            'group_name1': '私聊',
        }

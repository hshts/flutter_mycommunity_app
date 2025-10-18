from flask import request
from flask_restx import Namespace, Resource

from api.fields.user import get_user_models
from api.services.user_service import UserService
from api.utils.auth import token_required
import hashlib


ns = Namespace('user', description='用户相关接口')

models = get_user_models(ns)
user_model = models['user_model']
login_model = models['login_model']
mobile_login_model = models['mobile_login_model']
email_code_login_model = models['email_code_login_model']
email_code_validity_model = models['email_code_validity_model']
update_push_token_model = models['update_push_token_model']
update_mobile_model = models['update_mobile_model']
update_avatar_url_model = models['update_avatar_url_model']
update_sex_model = models['update_sex_model']
update_subject_model = models['update_subject_model']
update_birthday_model = models['update_birthday_model']
update_name_model = models['update_name_model']
update_location_model = models['update_location_model']
update_signature_model = models['update_signature_model']
update_password_model = models['update_password_model']
update_interest_model = models['update_interest_model']
update_voice_model = models['update_voice_model']
deltoken_model = models['deltoken_model']
not_interested_model = models['not_interested_model']
gp_not_interested_model = models['gp_not_interested_model']
blacklist_model = models['blacklist_model']
follow_model = models['follow_model']
response_model = models['response_model']


@ns.route('/login')
class UserLogin(Resource):
    # @ns.expect(login_model)
    def post(self):
        data = request.json or {}
        try:
            user = UserService.login(data.get('mobile'), data.get('email'), data.get('password'))
            usermap = user.to_dict() if user else {}
            ### ToDo:简化：生成token
            token =  hashlib.md5(str(usermap['uid']).encode('utf-8')).hexdigest()
            usermap['access_token'] = token
            usermap['token'] = token

            return {'data': usermap}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/sendMobileOTP')
class SendMobileOTP(Resource):
    def get(self):
        mobile = request.args.get('mobile')
        if not mobile:
            return {'error': 'Missing mobile'}, 400
        ok = UserService.send_mobile_otp(mobile)
        return {'data': ok}, 200


@ns.route('/email-code-login')
class EmailCodeLogin(Resource):
    @ns.expect(email_code_login_model)
    def post(self):
        data = request.json or {}
        email = data.get('email')
        if not email:
            return {'error': 'Missing email'}, 400
        token = UserService.email_code_login(email)
        return {'data': token}, 200


@ns.route('/sendVCodeByUid')
class SendVCodeByUid(Resource):
    @token_required
    def get(self):
        uid = request.args.get('uid', type=int)
        if not uid:
            return {'error': 'Missing uid'}, 400
        # 简化：直接返回成功
        return {'data': True}, 200


@ns.route('/loginmobile')
class LoginMobile(Resource):
    @ns.expect(mobile_login_model)
    def post(self):
        data = request.json or {}
        try:
            u = UserService.login_mobile(data.get('mobile'), data.get('vcode'), data.get('country'))
            return {'data': u.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/email-code-login/validity')
class EmailCodeLoginValidity(Resource):
    @ns.expect(email_code_validity_model)
    def post(self):
        data = request.json or {}
        try:
            u = UserService.email_code_login_validity(data.get('email'), data.get('code'), data.get('token'))
            return {'data': u.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/loginweixin')
class LoginWeixin(Resource):
    def post(self):
        # 简化：根据code创建或返回用户
        code = (request.json or {}).get('code')
        from api.models import User
        from api import db
        u = User.query.filter_by(weixin_openid=code).first() if code else None
        if not u:
            u = User(username='WeixinUser', weixin_openid=code)
            db.session.add(u)
            db.session.commit()
        return {'data': u.to_dict()}, 200


@ns.route('/loginios')
class LoginIOS(Resource):
    def post(self):
        data = request.json or {}
        identity_token = data.get('identityToken')
        ios_user_id = data.get('iosuserid')
        from api.models import User
        from api import db
        u = User.query.filter_by(ios_userid=ios_user_id).first() if ios_user_id else None
        if not u:
            u = User(username='IOSUser', ios_userid=ios_user_id)
            db.session.add(u)
            db.session.commit()
        return {'data': u.to_dict()}, 200


@ns.route('/updatePushToken')
class UpdatePushToken(Resource):
    @ns.expect(update_push_token_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_push_token(data.get('uid'), data.get('brand'), data.get('pushtoken'))
        return {'data': ok}, 200


@ns.route('/verifyVCode')
class VerifyVCode(Resource):
    @token_required
    def post(self):
        # 简化：总是返回成功
        return {'data': True}, 200


@ns.route('/updateMobile')
class UpdateMobile(Resource):
    @ns.expect(update_mobile_model)
    @token_required
    def post(self):
        data = request.json or {}
        try:
            u = UserService.update_mobile(data.get('uid'), data.get('vcode'), data.get('mobile'), data.get('country'), data.get('confirm'))
            return {'data': u.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/userexit')
class UserExit(Resource):
    @token_required
    def post(self):
        return {'data': True}, 200


@ns.route('/getProfile')
class Profile(Resource):
    def get(self):
        uid = request.args.get('uid')
        user = UserService.get_profile_by_uid(uid)
        userMap = user.to_dict()
        ### ToDo:简化：生成token
        token = hashlib.md5(str(userMap['uid']).encode('utf-8')).hexdigest()
        userMap['token'] = token
        userMap['access_token'] = token
        return {'data': userMap}, 200


@ns.route('/updateImage')
class UpdateImage(Resource):
    @token_required
    def post(self):
        uid = int(request.form.get('uid')) if request.form.get('uid') else None
        imagefile = request.files.get('imagefile')
        try:
            ok = UserService.update_avatar_file(uid, imagefile)
            return {'data': ok}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/AliPay/loginali')
class AliLogin(Resource):
    def post(self):
        # 简化：直接返回新用户
        from api.models import User
        u = User(username='AliUser')
        from api import db
        db.session.add(u)
        db.session.commit()
        return {'data': u.to_dict()}, 200


@ns.route('/AliPay/updateali')
class AliUpdate(Resource):
    @token_required
    def post(self):
        # 简化：直接返回用户
        from api.models import User
        uid = (request.json or {}).get('uid')
        u = User.query.get(uid)
        return {'data': u.to_dict() if u else {}}, 200


@ns.route('/updateweixin')
class UpdateWeixin(Resource):
    @token_required
    def post(self):
        from api.models import User
        uid = (request.json or {}).get('uid')
        u = User.query.get(uid)
        return {'data': u.to_dict() if u else {}}, 200


@ns.route('/updateios')
class UpdateIOS(Resource):
    @token_required
    def post(self):
        from api.models import User
        uid = (request.json or {}).get('uid')
        u = User.query.get(uid)
        return {'data': u.to_dict() if u else {}}, 200


@ns.route('/AliPay/userauth')
class AliUserAuth(Resource):
    def post(self):
        # 返回一个模拟的授权URL
        return {'data': 'https://alipay.example.com/auth?foo=bar'}, 200


@ns.route('/updateAvatar')
class AccountAvatar(Resource):
    @ns.expect(update_avatar_url_model)
    def post(self):
        data = request.json or {}
        # 假设通过token可取到uid，此处简化从参数里取
        uid = data.get('uid') or 1
        try:
            ok = UserService.update_avatar_url(uid, data.get('avatar'))
            return {'data': ok}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/updateSex')
class UpdateSex(Resource):
    @ns.expect(update_sex_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_sex(data.get('uid'), data.get('sex'))
        return {'data': ok}, 200


@ns.route('/updateSubject')
class UpdateSubject(Resource):
    @ns.expect(update_subject_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_subject(data.get('uid'), data.get('subject'))
        return {'data': ok}, 200


@ns.route('/updateBirthday')
class UpdateBirthday(Resource):
    @ns.expect(update_birthday_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_birthday(data.get('uid'), data.get('birthday'))
        return {'data': ok}, 200


@ns.route('/updateName')
class UpdateName(Resource):
    @ns.expect(update_name_model)
    def post(self):
        data = request.json or {}
        # 简化：uid从参数里取
        uid = data.get('uid') or 1
        ok = UserService.update_name(uid, data.get('name'))
        return {'data': ok}, 200


@ns.route('/updateLocation')
class UpdateLocation(Resource):
    @ns.expect(update_location_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_location(data.get('uid'), data.get('province'), data.get('city'))
        return {'data': ok}, 200


@ns.route('/updateSignature')
class UpdateSignature(Resource):
    @ns.expect(update_signature_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_signature(data.get('uid'), data.get('signature'))
        return {'data': ok}, 200


@ns.route('/updatePassword')
class UpdatePassword(Resource):
    # @ns.expect(update_password_model)
    def post(self):
        data = request.json or {}
        try:
            ok = UserService.update_password(data.get('token'), data.get('uid'), data.get('new_password'), data.get('repeat_new_password'))
            return {'data': ok}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@ns.route('/updateInterest')
class UpdateInterest(Resource):
    @ns.expect(update_interest_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_interest(data.get('uid'), data.get('interest'))
        return {'data': ok}, 200


@ns.route('/updateVoice')
class UpdateVoice(Resource):
    @ns.expect(update_voice_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.update_voice(data.get('uid'), data.get('voice'))
        return {'data': ok}, 200


@ns.route('/deltoken')
class DelToken(Resource):
    @ns.expect(deltoken_model)
    @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.deltoken(data.get('token'), data.get('uid'))
        return {'data': ok}, 200


@ns.route('/updateNotinteresteduids')
class UpdateNotInterestedUIDs(Resource):
    @ns.expect(not_interested_model)
    @token_required
    def post(self):
        data = request.json or {}
        ids = data.get('notinteresteduids') or []
        ok = UserService.update_notinterested_uids(data.get('uid'), ids)
        return {'data': ok}, 200


@ns.route('/goodpricenotinteresteduids')
class UpdateGoodPriceNotInterestedUIDs(Resource):
    @ns.expect(gp_not_interested_model)
    @token_required
    def post(self):
        data = request.json or {}
        ids = data.get('goodpricenotinteresteduids') or []
        ok = UserService.goodprice_notinterested_uids(data.get('uid'), ids)
        return {'data': ok}, 200


@ns.route('/updateBlacklist')
class UpdateBlacklist(Resource):
    @ns.expect(blacklist_model)
    ### TODO: token authentication
    # @token_required
    def post(self):
        data = request.json or {}
        ids = data.get('blacklist') or []
        ok = UserService.update_blacklist(data.get('uid'), ids)
        return {'data': ok}, 200


@ns.route('/getFollow')
class GetFollow(Resource):
    def post(self):
        uid = (request.json or {}).get('uid')
        if not uid:
            return {'error': 'Missing uid'}, 400
        data = UserService.get_follow(uid)
        return {'data': data}, 200


@ns.route('/selFollwerUser')
class SelFollowerUser(Resource):
    def post(self):
        data = request.json or {}
        ts = UserService.sel_follower_user(data.get('uid'), data.get('followed'))
        return {'data': ts}, 200


@ns.route('/follwerCommunity')
class FollwerCommunity(Resource):
    @ns.expect(follow_model)
    # @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.follow(data.get('uid'), data.get('followed'))
        return {'data': ok}, 200


@ns.route('/cleanfollwerCommunity')
class CleanFollwerCommunity(Resource):
    @ns.expect(follow_model)
    # @token_required
    def post(self):
        data = request.json or {}
        ok = UserService.follow(data.get('uid'), data.get('followed'), is_clean=True)
        return {'data': ok}, 200


@ns.route('/getuserinfo')
class GetUserInfo(Resource):
    def post(self):
        uid = (request.json or {}).get('uid')
        data = UserService.get_userinfo(uid)
        return {'data': data}, 200


@ns.route('/selUserDynamic')
class SelUserDynamic(Resource):
    def post(self):
        # 简化：返回空动态列表
        data = request.json or {}
        return {'data': [], 'currentIndex': data.get('currentIndex', 0)}, 200


@ns.route('/updateMemberJoin')
class UpdateMemberJoin(Resource):
    @token_required
    def post(self):
        # 发送加好友请求（简化为总是成功）
        return {'data': True}, 200


@ns.route('/updateSharedFriend')
class UpdateSharedFriend(Resource):
    @token_required
    def post(self):
        # 分享好友（简化为总是成功）
        return {'data': True}, 200


@ns.route('/getFollowUsers')
class GetFollowUsers(Resource):
    # @token_required
    def post(self):
        data = request.json or {}
        uid = data.get('uid')
        current_index = data.get('currentIndex', 0)
        users = UserService.get_follow_users(uid, current_index)
        return {'data': users}, 200


@ns.route('/getFollowUsersInCommunityALL')
class GetFollowUsersInCommunityALL(Resource):
    @token_required
    def post(self):
        data = request.json or {}
        uid = data.get('uid')
        current_index = data.get('currentIndex', 0)
        users = UserService.get_follow_users(uid, current_index)
        return {'data': users}, 200


@ns.route('/getFollowUsersCommunity')
class GetFollowUsersCommunity(Resource):
    def post(self):
        data = request.json or {}
        uid = data.get('uid')
        current_index = data.get('currentIndex', 0)
        users = UserService.get_follow_users(uid, current_index)
        return {'data': users}, 200


@ns.route('/getFansUsers')
class GetFansUsers(Resource):
    def post(self):
        data = request.json or {}
        uid = data.get('uid')
        current_index = data.get('currentIndex', 0)
        users = UserService.get_fans_users(uid, current_index)
        return {'data': users}, 200


@ns.route('/getSingleConversation')
class GetSingleConversation(Resource):
    @token_required
    def post(self):
        data = request.json or {}
        res = UserService.get_single_conversation(data.get('uid'), data.get('touid'), data.get('timeline_id'))
        return {'data': res}, 200


@ns.route('/joinSingle')
class JoinSingle(Resource):
    @token_required
    def post(self):
        data = request.json or {}
        res = UserService.get_single_conversation(data.get('uid'), data.get('touid'), data.get('timeline_id'))
        return {'data': res}, 200

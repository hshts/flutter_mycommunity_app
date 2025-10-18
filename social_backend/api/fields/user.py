from flask_restx import fields


def get_user_models(ns):
    user_model = ns.model('User', {
        'uid': fields.Integer(description='用户ID'),
        'username': fields.String(description='用户名'),
        'mobile': fields.String(description='手机号'),
        'email': fields.String(description='邮箱'),
        'sex': fields.String(description='性别'),
        'birthday': fields.String(description='生日'),
        'province': fields.String(description='省份'),
        'city': fields.String(description='城市'),
        'signature': fields.String(description='个人简介'),
        'interest': fields.String(description='兴趣'),
        'voice': fields.String(description='录音'),
        'profilepicture': fields.String(description='头像'),
        'usertype': fields.Integer(description='用户类型'),
    })

    login_model = ns.model('UserLogin', {
        'mobile': fields.String(description='手机号'),
        'email': fields.String(description='邮箱'),
        'password': fields.String(description='密码(MD5或明文，示例用途)')
    })

    mobile_login_model = ns.model('MobileLogin', {
        'mobile': fields.String(required=True, description='手机号'),
        'vcode': fields.String(required=True, description='验证码'),
        'country': fields.String(description='国家代码')
    })

    email_code_login_model = ns.model('EmailCodeLogin', {
        'email': fields.String(required=True, description='邮箱')
    })

    email_code_validity_model = ns.model('EmailCodeLoginValidity', {
        'email': fields.String(required=True),
        'code': fields.String(required=True),
        'token': fields.String(required=True),
    })

    update_push_token_model = ns.model('UpdatePushToken', {
        'uid': fields.Integer(required=True),
        'token': fields.String(required=True),
        'brand': fields.String(required=True),
        'pushtoken': fields.String(required=True),
    })

    update_mobile_model = ns.model('UpdateMobile', {
        'uid': fields.Integer(required=True),
        'token': fields.String(required=True),
        'vcode': fields.String(required=True),
        'mobile': fields.String(required=True),
        'country': fields.String,
        'confirm': fields.Integer,
    })

    update_avatar_url_model = ns.model('UpdateAvatarUrl', {
        'avatar': fields.String(required=True, description='头像URL')
    })

    update_sex_model = ns.model('UpdateSex', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'sex': fields.String(required=True)
    })

    update_subject_model = ns.model('UpdateSubject', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'subject': fields.String(required=True)
    })

    update_birthday_model = ns.model('UpdateBirthday', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'birthday': fields.String(required=True)
    })

    update_name_model = ns.model('UpdateName', {
        'name': fields.String(required=True)
    })

    update_location_model = ns.model('UpdateLocation', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'province': fields.String(required=True),
        'city': fields.String(required=True),
    })

    update_signature_model = ns.model('UpdateSignature', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'signature': fields.String(required=True),
    })

    update_password_model = ns.model('UpdatePassword', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'new_password': fields.String(required=True),
        'repeat_new_password': fields.String(required=True),
    })

    update_interest_model = ns.model('UpdateInterest', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'interest': fields.String(required=True),
    })

    update_voice_model = ns.model('UpdateVoice', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'voice': fields.String(required=True),
    })

    deltoken_model = ns.model('DelToken', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
    })

    not_interested_model = ns.model('NotInterested', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'notinteresteduids': fields.List(fields.Integer, required=True),
    })

    gp_not_interested_model = ns.model('GoodPriceNotInterested', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'goodpricenotinteresteduids': fields.List(fields.Integer, required=True),
    })

    blacklist_model = ns.model('UpdateBlacklist', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'blacklist': fields.List(fields.Integer, required=True),
    })

    follow_model = ns.model('Follow', {
        'token': fields.String(required=True),
        'uid': fields.Integer(required=True),
        'followed': fields.Integer(required=True),
    })

    single_conversation_model = ns.model('SingleConversation', {
        'token': fields.String(required=True),
        'touid': fields.Integer(required=True),
        'uid': fields.Integer(required=True),
        'timeline_id': fields.String(required=True),
        'captchaVerification': fields.String,
        'isCustomer': fields.Integer,
    })

    response_model = ns.model('UserResponse', {
        'data': fields.Raw,
        'error': fields.String,
        'success': fields.Boolean,
        'message': fields.String,
    })

    return {
        'user_model': user_model,
        'login_model': login_model,
        'mobile_login_model': mobile_login_model,
        'email_code_login_model': email_code_login_model,
        'email_code_validity_model': email_code_validity_model,
        'update_push_token_model': update_push_token_model,
        'update_mobile_model': update_mobile_model,
        'update_avatar_url_model': update_avatar_url_model,
        'update_sex_model': update_sex_model,
        'update_subject_model': update_subject_model,
        'update_birthday_model': update_birthday_model,
        'update_name_model': update_name_model,
        'update_location_model': update_location_model,
        'update_signature_model': update_signature_model,
        'update_password_model': update_password_model,
        'update_interest_model': update_interest_model,
        'update_voice_model': update_voice_model,
        'deltoken_model': deltoken_model,
        'not_interested_model': not_interested_model,
        'gp_not_interested_model': gp_not_interested_model,
        'blacklist_model': blacklist_model,
        'follow_model': follow_model,
        'single_conversation_model': single_conversation_model,
        'response_model': response_model,
    }

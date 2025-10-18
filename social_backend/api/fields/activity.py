from flask_restx import fields

def get_activity_models(ns):
    """注册并返回所有活动相关的模型到命名空间"""
    
    activity_model = ns.model('Activity', {
        'actid': fields.String(required=False, description='活动ID'),
        'content': fields.String(required=True, description='活动内容'),
        'createtime': fields.DateTime(required=False, description='创建时间'),
        'updatetime': fields.DateTime(required=False, description='更新时间'),
        'status': fields.Integer(required=False, description='活动状态'),
        'peoplenum': fields.Integer(required=False, description='活动总人数'),
        'currentpeoplenum': fields.Integer(required=False, description='当前参与人数'),
        'startyear': fields.Integer(required=False, description='开始时间戳'),
        'endyear': fields.Integer(required=False, description='结束时间戳'),
        'address': fields.String(required=False, description='活动地址'),
        'addresstitle': fields.String(required=False, description='地址标题'),
        'lat': fields.Float(required=False, description='纬度'),
        'lng': fields.Float(required=False, description='经度'),
        'actcity': fields.String(required=False, description='活动城市'),
        'actprovince': fields.String(required=False, description='活动省份'),
        'coverimg': fields.String(required=False, description='封面图片'),
        'coverimgwh': fields.String(required=False, description='封面图片宽高比'),
        'actimagespath': fields.String(required=False, description='活动图片路径列表'),
        'maxcost': fields.Float(required=False, description='最大费用'),
        'mincost': fields.Float(required=False, description='最小费用'),
        'paytype': fields.Integer(required=False, description='支付类型'),
        'uid': fields.Integer(required=True, description='发起人用户ID'),
        'goodpriceid': fields.String(required=False, description='关联商品ID'),
        'likenum': fields.Integer(required=False, description='点赞数'),
        'collectionnum': fields.Integer(required=False, description='收藏数'),
        'commentnum': fields.Integer(required=False, description='评论数'),
        'viewnum': fields.Integer(required=False, description='浏览数'),
        'joinnum': fields.Integer(required=False, description='参与数'),
        'locked': fields.Integer(required=False, description='是否锁定(活动开始)')
    })

    create_activity_model = ns.model('CreateActivity', {
        'content': fields.String(required=True, description='活动内容'),
        'uid': fields.Integer(required=True, description='发起人用户ID'),
        'province': fields.String(required=False, description='活动省份'),
        'city': fields.String(required=False, description='活动城市'),
        'address': fields.String(required=False, description='活动地址'),
        'addresstitle': fields.String(required=False, description='地址标题'),
        'lat': fields.Float(required=False, description='纬度'),
        'lng': fields.Float(required=False, description='经度'),
        'coverimg': fields.String(required=False, description='封面图片'),
        'coverimgWH': fields.String(required=False, description='封面图片宽高比'),
        'startyear': fields.Integer(required=False, description='开始时间戳'),
        'endyear': fields.Integer(required=False, description='结束时间戳'),
        'paytype': fields.Integer(required=False, description='支付类型'),
        'goodpriceid': fields.String(required=False, description='关联商品ID')
    })

    user_activity_model = ns.model('UserActivity', {
        'actid': fields.String(required=True, description='活动ID'),
        'uid': fields.Integer(required=True, description='用户ID')
    })

    activity_time_model = ns.model('ActivityTime', {
        'actid': fields.String(required=True, description='活动ID'),
        'uid': fields.Integer(required=True, description='用户ID'),
        'startyear': fields.Integer(required=True, description='开始时间戳'),
        'endyear': fields.Integer(required=True, description='结束时间戳')
    })

    activity_status_model = ns.model('ActivityStatus', {
        'actid': fields.String(required=True, description='活动ID'),
        'uid': fields.Integer(required=True, description='用户ID'),
        'status': fields.Integer(required=True, description='活动状态')
    })

    activity_comment_model = ns.model('ActivityComment', {
        'actid': fields.String(required=True, description='活动ID'),
        'uid': fields.Integer(required=True, description='用户ID'),
        'content': fields.String(required=True, description='评论内容')
    })

    delete_comment_model = ns.model('DeleteComment', {
        'actid': fields.String(required=True, description='活动ID'),
        'uid': fields.Integer(required=True, description='用户ID'),
        'commentid': fields.Integer(required=True, description='评论ID')
    })

    group_conversation_model = ns.model('GroupConversation', {
        'timeline_id': fields.String(required=True, description='时间线ID'),
        'uid': fields.Integer(required=True, description='用户ID')
    })

    response_model = ns.model('Response', {
        'data': fields.Raw(description='响应数据'),
        'error': fields.String(description='错误信息')
    })

    return {
        'activity_model': activity_model,
        'create_activity_model': create_activity_model,
        'user_activity_model': user_activity_model,
        'activity_time_model': activity_time_model,
        'activity_status_model': activity_status_model,
        'activity_comment_model': activity_comment_model,
        'delete_comment_model': delete_comment_model,
        'group_conversation_model': group_conversation_model,
        'response_model': response_model
    }

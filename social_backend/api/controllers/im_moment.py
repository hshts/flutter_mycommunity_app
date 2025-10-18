"""IM模块 - Moment(动态)相关接口"""
from flask import request
from flask_restx import Namespace, Resource, fields
from api.services.moment_service import MomentService
from api.utils.auth import token_required

# 创建命名空间
ns = Namespace('IM', description='IM模块 - 动态相关接口')

# 定义请求和响应模型
moment_create_model = ns.model('MomentCreate', {
    'uid': fields.Integer(required=True, description='用户ID'),
    'token': fields.String(required=True, description='用户认证令牌'),
    'content': fields.String(required=True, description='动态内容'),
    'voice': fields.String(description='音频文件路径'),
    'images': fields.String(description='图片列表(JSON)'),
    'coverimgwh': fields.String(description='封面图宽高比'),
    'category': fields.String(description='分类/话题'),
    'captchaVerification': fields.String(description='验证码')
})

moment_delete_model = ns.model('MomentDelete', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'momentid': fields.Integer(required=True, description='动态ID')
})

moment_list_model = ns.model('MomentList', {
    'currIndex': fields.Integer(description='当前索引', default=0),
    'subject': fields.String(description='主题/话题')
})

moment_info_model = ns.model('MomentInfo', {
    'momentid': fields.Integer(required=True, description='动态ID')
})

moment_user_list_model = ns.model('MomentUserList', {
    'uid': fields.Integer(required=True, description='用户ID')
})

moment_search_model = ns.model('MomentSearch', {
    'content': fields.String(required=True, description='搜索内容'),
    'currentIndex': fields.Integer(description='当前索引', default=0)
})

moment_like_model = ns.model('MomentLike', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'momentid': fields.Integer(required=True, description='动态ID'),
    'uid': fields.Integer(required=True, description='用户ID')
})

moment_comment_model = ns.model('MomentComment', {
    'commentid': fields.Integer(description='评论ID(回复时使用)'),
    'token': fields.String(required=True, description='用户认证令牌'),
    'momentid': fields.Integer(required=True, description='动态ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'touid': fields.Integer(description='目标用户ID'),
    'content': fields.String(required=True, description='评论内容'),
    'captchaVerification': fields.String(description='验证码')
})

moment_comment_delete_model = ns.model('MomentCommentDelete', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'commentid': fields.Integer(required=True, description='评论ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'replyid': fields.Integer(description='回复ID'),
    'momentid': fields.Integer(required=True, description='动态ID')
})

moment_comment_list_model = ns.model('MomentCommentList', {
    'momentid': fields.Integer(required=True, description='动态ID')
})

moment_comment_like_model = ns.model('MomentCommentLike', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'commentid': fields.Integer(required=True, description='评论ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'likeuid': fields.Integer(description='被点赞用户ID'),
    'momentid': fields.Integer(description='动态ID')
})

moment_comment_unlike_model = ns.model('MomentCommentUnlike', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'commentid': fields.Integer(required=True, description='评论ID'),
    'likeuid': fields.Integer(description='被点赞用户ID'),
    'uid': fields.Integer(required=True, description='用户ID')
})


@ns.route('/reportMoment')
class ReportMoment(Resource):
    """发布动态"""
    
    @ns.doc('report_moment')
    @ns.expect(moment_create_model)
    def post(self):
        """发布动态"""
        try:
            data = request.get_json()
            
            momentid = MomentService.create_moment(
                uid=data.get('uid'),
                content=data.get('content'),
                voice=data.get('voice'),
                images=data.get('images'),
                coverimgwh=data.get('coverimgwh'),
                category=data.get('category')
            )
            
            return {
                'code': 200,
                'msg': '发布成功',
                'data': {'momentid': momentid}
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'发布失败: {str(e)}',
                'data': None
            }


@ns.route('/delMoment')
class DelMoment(Resource):
    """删除动态"""
    
    @ns.doc('delete_moment')
    @ns.expect(moment_delete_model)
    def post(self):
        """删除动态"""
        try:
            data = request.get_json()
            
            success = MomentService.delete_moment(
                momentid=data.get('momentid'),
                uid=data.get('uid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '删除成功',
                    'data': True
                }
            else:
                return {
                    'code': 404,
                    'msg': '动态不存在或无权删除',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'删除失败: {str(e)}',
                'data': False
            }


@ns.route('/getMomentList')
class GetMomentList(Resource):
    """获取动态列表"""
    
    @ns.doc('get_moment_list')
    # @ns.expect(moment_list_model)
    def post(self):
        """获取动态列表"""
        try:
            data = request.get_json()
            
            moments = MomentService.get_moment_list(
                currentIndex=data.get('currIndex', 0),
                subject=data.get('subject')
            )
            
            return {
                'code': 200,
                'msg': '获取成功',
                'data': moments,
                'total':len(moments),
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'获取失败: {str(e)}',
                'data': None
            }


@ns.route('/getMomentInfo')
class GetMomentInfo(Resource):
    """获取动态详情"""
    
    @ns.doc('get_moment_info')
    @ns.expect(moment_info_model)
    def post(self):
        """获取动态详情"""
        try:
            data = request.get_json()
            
            moment = MomentService.get_moment_info(
                momentid=data.get('momentid')
            )
            
            if moment:
                return {
                    'code': 200,
                    'msg': '获取成功',
                    'data': moment
                }
            else:
                return {
                    'code': 404,
                    'msg': '动态不存在',
                    'data': None
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'获取失败: {str(e)}',
                'data': None
            }


@ns.route('/getMomentListByUser')
class GetMomentListByUser(Resource):
    """获取用户动态列表"""
    
    @ns.doc('get_moment_list_by_user')
    @ns.expect(moment_user_list_model)
    def post(self):
        """获取用户动态列表"""
        try:
            data = request.get_json()
            
            moments = MomentService.get_moment_list_by_user(
                uid=data.get('uid')
            )
            
            return {
                'code': 200,
                'msg': '获取成功',
                'data': moments,
                'total': len(moments),
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'获取失败: {str(e)}',
                'data': None
            }


@ns.route('/searchMoment')
class SearchMoment(Resource):
    """搜索动态"""
    
    @ns.doc('search_moment')
    @ns.expect(moment_search_model)
    def post(self):
        """搜索动态"""
        try:
            data = request.get_json()
            
            moments = MomentService.search_moment(
                content=data.get('content'),
                currentIndex=data.get('currentIndex', 0)
            )
            
            return {
                'code': 200,
                'msg': '搜索成功',
                'data': {'list': moments, 'total': len(moments)}
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'搜索失败: {str(e)}',
                'data': None
            }


@ns.route('/updateMomentLike')
class UpdateMomentLike(Resource):
    """动态点赞"""
    
    @ns.doc('update_moment_like')
    @ns.expect(moment_like_model)
    def post(self):
        """动态点赞"""
        try:
            data = request.get_json()
            
            success = MomentService.add_moment_like(
                momentid=data.get('momentid'),
                uid=data.get('uid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '点赞成功',
                    'data': True
                }
            else:
                return {
                    'code': 201,
                    'msg': '已经点赞过了',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'点赞失败: {str(e)}',
                'data': False
            }


@ns.route('/delMomentLike')
class DelMomentLike(Resource):
    """取消动态点赞"""
    
    @ns.doc('delete_moment_like')
    @ns.expect(moment_like_model)
    def post(self):
        """取消动态点赞"""
        try:
            data = request.get_json()
            
            success = MomentService.remove_moment_like(
                momentid=data.get('momentid'),
                uid=data.get('uid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '取消点赞成功',
                    'data': True
                }
            else:
                return {
                    'code': 404,
                    'msg': '点赞记录不存在',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'取消点赞失败: {str(e)}',
                'data': False
            }


@ns.route('/updateMomentComment')
class UpdateMomentComment(Resource):
    """发布动态评论"""
    
    @ns.doc('update_moment_comment')
    @ns.expect(moment_comment_model)
    def post(self):
        """发布动态评论"""
        try:
            data = request.get_json()
            
            result_id = MomentService.add_moment_comment(
                momentid=data.get('momentid'),
                uid=data.get('uid'),
                touid=data.get('touid'),
                content=data.get('content'),
                commentid=data.get('commentid')
            )
            
            return {
                'code': 200,
                'msg': '评论成功',
                'data': {'id': result_id}
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'评论失败: {str(e)}',
                'data': None
            }


@ns.route('/delMomentComment')
class DelMomentComment(Resource):
    """删除动态评论"""
    
    @ns.doc('delete_moment_comment')
    @ns.expect(moment_comment_delete_model)
    def post(self):
        """删除动态评论"""
        try:
            data = request.get_json()
            
            success = MomentService.delete_moment_comment(
                commentid=data.get('commentid'),
                uid=data.get('uid'),
                replyid=data.get('replyid'),
                momentid=data.get('momentid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '删除成功',
                    'data': True
                }
            else:
                return {
                    'code': 404,
                    'msg': '评论不存在或无权删除',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'删除失败: {str(e)}',
                'data': False
            }


@ns.route('/getMomentComment')
class GetMomentComment(Resource):
    """获取动态评论列表"""
    
    @ns.doc('get_moment_comment', params={
        'momentid': {'description': '动态ID', 'type': 'integer', 'required': True}
    })
    def get(self):
        """获取动态评论列表"""
        try:
            momentid = request.args.get('momentid', type=int)
            
            if not momentid:
                return {
                    'code': 400,
                    'msg': '缺少必要参数momentid',
                    'data': None
                }
            
            comments = MomentService.get_moment_comment_list(momentid=momentid)
            
            return {
                'code': 200,
                'msg': '获取成功',
                'data': comments,
                'total': len(comments),
            }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'获取失败: {str(e)}',
                'data': None
            }


@ns.route('/updateMomentCommentLike')
class UpdateMomentCommentLike(Resource):
    """动态评论点赞"""
    
    @ns.doc('update_moment_comment_like')
    @ns.expect(moment_comment_like_model)
    def post(self):
        """动态评论点赞"""
        try:
            data = request.get_json()
            
            success = MomentService.add_moment_comment_like(
                commentid=data.get('commentid'),
                uid=data.get('uid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '点赞成功',
                    'data': True
                }
            else:
                return {
                    'code': 201,
                    'msg': '已经点赞过了',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'点赞失败: {str(e)}',
                'data': False
            }


@ns.route('/delMomentCommentLike')
class DelMomentCommentLike(Resource):
    """取消动态评论点赞"""
    
    @ns.doc('delete_moment_comment_like')
    @ns.expect(moment_comment_unlike_model)
    def post(self):
        """取消动态评论点赞"""
        try:
            data = request.get_json()
            
            success = MomentService.remove_moment_comment_like(
                commentid=data.get('commentid'),
                uid=data.get('uid')
            )
            
            if success:
                return {
                    'code': 200,
                    'msg': '取消点赞成功',
                    'data': True
                }
            else:
                return {
                    'code': 404,
                    'msg': '点赞记录不存在',
                    'data': False
                }
        except Exception as e:
            return {
                'code': 500,
                'msg': f'取消点赞失败: {str(e)}',
                'data': False
            }

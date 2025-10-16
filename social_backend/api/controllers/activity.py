from flask import request
from flask_restx import Resource, Namespace
from api.services.activity_service import ActivityService
from api.services.comment_service import CommentService
from api.fields.activity import get_activity_models
from api.utils.auth import token_required

# 创建命名空间
ns = Namespace('Activity', description='Activity operations')

# 获取所有模型
models = get_activity_models(ns)
activity_fields = models['activity_fields']
create_activity_fields = models['create_activity_fields']
user_activity_fields = models['user_activity_fields']
activity_time_fields = models['activity_time_fields']
activity_status_fields = models['activity_status_fields']
activity_comment_fields = models['activity_comment_fields']
delete_comment_fields = models['delete_comment_fields']
group_conversation_fields = models['group_conversation_fields']
response_fields = models['response_fields']


@ns.route('/createActivity')
class CreateActivity(Resource):
    @ns.doc('create_activity')
    @ns.expect(create_activity_fields)
    @ns.response(201, 'Activity created', activity_fields)
    @ns.response(400, 'Validation error', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    # @token_required
    def post(self):
        """创建活动"""
        try:
            data = request.json
            activity = ActivityService.create_activity(data)
            return activity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 500
        
@ns.route('/getActivityTypeList')
class GetActivityTypeList(Resource):
    @ns.doc('get_activity_type_list')
    @ns.response(200, 'Activity type list', [activity_fields])
    @ns.response(500, 'Internal server error', response_fields)
    def get(self):
        """获取活动类型列表"""
        try:
            activity_types = {"data": [{'typename': 'type1'}, {'typename': 'type2'}]}  # 示例数据
            return activity_types, 200
        except Exception as e:
            return {'error': str(e)}, 500



@ns.route('/getActivity')
class GetActivity(Resource):
    @ns.doc('get_activity')
    @ns.param('actid', 'Activity ID')
    @ns.response(200, 'Activity found', activity_fields)
    @ns.response(400, 'Missing actid parameter', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    def get(self):
        """获取活动详情"""
        try:
            actid = request.args.get('actid')
            if not actid:
                return {'error': 'Missing actid parameter'}, 400
                
            activity = ActivityService.get_activity_by_id(actid)
            if not activity:
                return {'error': 'Activity not found'}, 404

            return  { 'data':activity} , 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getActivityListByUpdateTime')
class GetActivitiesByUpdateTime(Resource):
    @ns.doc('get_activities_by_update_time')
    @ns.param('currentIndex', 'Current index for pagination')
    @ns.param('citycode', 'City code for filtering')
    @ns.response(200, 'Activities list', [activity_fields])
    @ns.response(500, 'Internal server error', response_fields)
    def get(self):
        """根据更新时间获取活动列表"""
        try:
            current_index = int(request.args.get('currentIndex', 0))
            citycode = request.args.get('citycode')
            
            activities = ActivityService.get_activities_by_update_time(
                current_index=current_index,
                citycode=citycode
            )
            return {
                'data':activities, #[activity.to_dict() for activity in activities],
                'citycode': citycode,
                'currentIndex': current_index,
                'count': len(activities)
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getActivityListByCity')
class GetActivitiesByCity(Resource):
    @ns.doc('get_activities_by_city')
    @ns.param('citycode', 'City code (required)', default='all')
    @ns.param('currentIndex', 'Current index for pagination', default=0)
    @ns.param('pageSize', 'Page size', default=20)
    @ns.param('orderBy', 'Order by field: updatetime, createtime, likenum, viewnum', default='updatetime')
    @ns.response(200, 'Activities list', [activity_fields])
    @ns.response(400, 'Missing citycode parameter', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    def get(self):
        """根据城市获取活动列表"""
        try:
            citycode = request.args.get('citycode')
            # if not citycode:
            #     return {'error': 'Missing citycode parameter'}, 400
            
            current_index = int(request.args.get('currentIndex', 0))
            page_size = int(request.args.get('pageSize', 20))
            order_by = request.args.get('orderBy', 'updatetime')
            
            # 验证排序字段
            valid_order_fields = ['updatetime', 'createtime', 'likenum', 'viewnum']
            if order_by not in valid_order_fields:
                order_by = 'updatetime'
            
            activities = ActivityService.get_activities_by_city(
                citycode=citycode,
                current_index=current_index,
                page_size=page_size,
                order_by=order_by
            )
            
            return {
                'data': activities, #[activity.to_dict() for activity in activities],
                'citycode': citycode,
                'currentIndex': current_index,
                'pageSize': page_size,
                'count': len(activities)
            }, 200
        except ValueError as e:
            return {'error': 'Invalid parameter format'}, 400
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getActivityListByUser')
class GetActivitiesByUser(Resource):
    @ns.doc('get_activities_by_user')
    @ns.param('currentIndex', 'Current index for pagination')
    @ns.param('uid', 'User ID')
    @ns.response(200, 'Activities list', [activity_fields])
    @ns.response(400, 'Missing uid parameter', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    def get(self):
        """根据用户获取活动列表"""
        try:
            current_index = int(request.args.get('currentIndex', 0))
            uid = request.args.get('uid')
            
            if not uid:
                return {'error': 'Missing uid parameter'}, 400
            
            activities = ActivityService.get_activities_by_user(
                current_index=current_index,
                uid=uid
            )
            return [activity.to_dict() for activity in activities], 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getJoinActivityListByUser')
class GetJoinActivitiesByUser(Resource):
    @ns.doc('get_join_activities_by_user')
    @ns.param('currentIndex', 'Current index for pagination')
    @ns.param('uid', 'User ID')
    @ns.response(200, 'Activities list', [activity_fields])
    @ns.response(400, 'Missing uid parameter', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def get(self):
        """获取用户参与的活动列表"""
        try:
            current_index = int(request.args.get('currentIndex', 0))
            uid = request.args.get('uid')
            
            if not uid:
                return {'error': 'Missing uid parameter'}, 400
            
            activities = ActivityService.get_join_activities_by_user(
                current_index=current_index,
                uid=uid
            )
            return [activity.to_dict() for activity in activities], 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateLike')
class UpdateLike(Resource):
    @ns.doc('update_like')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Like updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """活动点赞"""
        try:
            data = request.json
            activity = ActivityService.update_like(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/delLike')
class DelLike(Resource):
    @ns.doc('delete_like')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Like deleted', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """活动取消点赞"""
        try:
            data = request.json
            activity = ActivityService.del_like(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateCollection')
class UpdateCollection(Resource):
    @ns.doc('update_collection')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Collection updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """活动收藏"""
        try:
            data = request.json
            activity = ActivityService.update_collection(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/delCollection')
class DelCollection(Resource):
    @ns.doc('delete_collection')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Collection deleted', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """活动取消收藏"""
        try:
            data = request.json
            activity = ActivityService.del_collection(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updatecomment')
class UpdateComment(Resource):
    @ns.doc('update_comment')
    @ns.expect(activity_comment_fields)
    @ns.response(200, 'Comment updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """发布活动评论"""
        try:
            data = request.json
            activity = ActivityService.update_comment(
                data['actid'], 
                data['uid'], 
                data['content']
            )
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            comment_id = 1
            return {'data': comment_id}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/delcomment')
class DelComment(Resource):
    @ns.doc('delete_comment')
    @ns.expect(delete_comment_fields)
    @ns.response(200, 'Comment deleted', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """删除活动评论"""
        try:
            data = request.json
            activity = ActivityService.del_comment(
                data['actid'], 
                data['uid'], 
                data['commentid']
            )
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/joinActivity')
class JoinActivity(Resource):
    @ns.doc('join_activity')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Joined activity', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """参加活动"""
        try:
            data = request.json
            activity = ActivityService.join_activity(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            group_relation = {
                'timeline_id': activity.actid,
                'uid': data['uid']
            }
            return {'data': group_relation}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/delActivity')
class DelActivity(Resource):
    @ns.doc('delete_activity')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Activity deleted', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """删除活动"""
        try:
            data = request.json
            result = ActivityService.del_activity(data['actid'], data['uid'])
            if not result:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateActivityTime')
class UpdateActivityTime(Resource):
    @ns.doc('update_activity_time')
    @ns.expect(activity_time_fields)
    @ns.response(200, 'Activity time updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """更新活动时间"""
        try:
            data = request.json
            activity = ActivityService.update_activity_time(
                data['actid'], 
                data['uid'], 
                data['startyear'], 
                data['endyear']
            )
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateActivity')
class UpdateActivity(Resource):
    @ns.doc('update_activity')
    @ns.expect(activity_fields)
    @ns.response(200, 'Activity updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """更新活动信息"""
        try:
            data = request.json
            activity = ActivityService.update_activity(
                data['actid'],
                data['uid'],
                data['content'],
                address=data.get('address'),
                addresstitle=data.get('addresstitle'),
                lat=data.get('lat'),
                lng=data.get('lng'),
                coverimg=data.get('coverimg'),
                coverimgwh=data.get('coverimgwh'),
                actimagespath=data.get('actimagespath')
            )
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateActivityStatus')
class UpdateActivityStatus(Resource):
    @ns.doc('update_activity_status')
    @ns.expect(activity_status_fields)
    @ns.response(200, 'Activity status updated', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """更新活动状态"""
        try:
            data = request.json
            activity = ActivityService.update_activity_status(
                data['actid'], 
                data['uid'], 
                data['status']
            )
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': True}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/exitActivity')
class ExitActivity(Resource):
    @ns.doc('exit_activity')
    @ns.expect(user_activity_fields)
    @ns.response(200, 'Exited activity', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """退出活动"""
        try:
            data = request.json
            activity = ActivityService.exit_activity(data['actid'], data['uid'])
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            return {'data': 1}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getGroupConversation')
class GetGroupConversation(Resource):
    @ns.doc('get_group_conversation')
    @ns.expect(group_conversation_fields)
    @ns.response(200, 'Group conversation info', response_fields)
    @ns.response(400, 'Missing required fields', response_fields)
    @ns.response(404, 'Activity not found', response_fields)
    @ns.response(500, 'Internal server error', response_fields)
    @token_required
    def post(self):
        """获取群聊信息"""
        try:
            data = request.json
            group_relation = ActivityService.get_group_conversation(
                data['timeline_id'], 
                data['uid']
            )
            if not group_relation:
                return {'error': 'Activity not found'}, 404
            
            return {'data': group_relation}, 200
        except Exception as e:
            return {'error': str(e)}, 500


# ============= 评论相关接口 =============

@ns.route('/getCommentList')
class GetCommentList(Resource):
    @ns.doc('get_comment_list')
    @ns.param('actid', 'Activity ID', required=True)
    @ns.param('uid', 'User ID (optional)')
    @ns.response(200, 'Comment list retrieved successfully')
    @ns.response(400, 'Missing actid parameter')
    @ns.response(500, 'Internal server error')
    def get(self):
        """获取活动评论列表"""
        try:
            actid = request.args.get('actid')
            if not actid:
                return {'error': 'Missing actid parameter'}, 400
            
            uid = request.args.get('uid', type=int)
            
            comments = CommentService.get_comment_list(actid, uid)
            return {'data': comments, 'count': len(comments)}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getReplyList')
class GetReplyList(Resource):
    @ns.doc('get_reply_list')
    @ns.param('commentid', 'Comment ID', required=True)
    @ns.response(200, 'Reply list retrieved successfully')
    @ns.response(400, 'Missing commentid parameter')
    @ns.response(500, 'Internal server error')
    def get(self):
        """获取评论回复列表"""
        try:
            commentid = request.args.get('commentid')
            if not commentid:
                return {'error': 'Missing commentid parameter'}, 400
            
            replies = CommentService.get_reply_list(commentid)
            return {'data': replies, 'count': len(replies)}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getNewCommentList')
class GetNewCommentList(Resource):
    @ns.doc('get_new_comment_list')
    @ns.response(200, 'New comment list retrieved successfully')
    @ns.response(400, 'Missing required parameters')
    @ns.response(500, 'Internal server error')
    def post(self):
        """获取新评论列表"""
        try:
            data = request.json
            actid = data.get('actid')
            if not actid:
                return {'error': 'Missing actid parameter'}, 400
            
            commentid = data.get('commentid')
            
            comments = CommentService.get_new_comment_list(actid, commentid)
            return {'data': comments, 'count': len(comments)}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getReply')
class GetReply(Resource):
    @ns.doc('get_reply')
    @ns.param('replyid', 'Reply ID', required=True)
    @ns.response(200, 'Reply retrieved successfully')
    @ns.response(400, 'Missing replyid parameter')
    @ns.response(404, 'Reply not found')
    @ns.response(500, 'Internal server error')
    def get(self):
        """获取指定回复"""
        try:
            replyid = request.args.get('replyid')
            if not replyid:
                return {'error': 'Missing replyid parameter'}, 400
            
            reply = CommentService.get_reply(replyid)
            if not reply:
                return {'error': 'Reply not found'}, 404
            
            return {'data': reply}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/getCommentReplyList')
class GetCommentReplyList(Resource):
    @ns.doc('get_comment_reply_list')
    @ns.response(200, 'Comment reply list retrieved successfully')
    @ns.response(400, 'Missing required parameters')
    @ns.response(500, 'Internal server error')
    def post(self):
        """获取评论回复列表（用于获取用户相关的回复）"""
        try:
            data = request.json
            uid = data.get('uid')
            if not uid:
                return {'error': 'Missing uid parameter'}, 400
            
            replyid = data.get('replyid')
            
            replies = CommentService.get_comment_reply_list(uid, replyid)
            return {'data': replies, 'count': len(replies)}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/updateCommentLike')
class UpdateCommentLike(Resource):
    @ns.doc('update_comment_like')
    @ns.response(200, 'Comment liked successfully')
    @ns.response(400, 'Missing required parameters')
    @ns.response(500, 'Internal server error')
    @token_required
    def post(self):
        """评论点赞"""
        try:
            data = request.json
            commentid = data.get('commentid')
            uid = data.get('uid')
            likeuid = data.get('likeuid')
            actid = data.get('actid')
            
            if not all([commentid, uid, likeuid, actid]):
                return {'error': 'Missing required parameters'}, 400
            
            success = CommentService.add_comment_like(commentid, uid, likeuid, actid)
            return {'data': success}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@ns.route('/delCommentLike')
class DelCommentLike(Resource):
    @ns.doc('del_comment_like')
    @ns.response(200, 'Comment like removed successfully')
    @ns.response(400, 'Missing required parameters')
    @ns.response(500, 'Internal server error')
    @token_required
    def post(self):
        """取消评论点赞"""
        try:
            data = request.json
            commentid = data.get('commentid')
            uid = data.get('uid')
            
            if not all([commentid, uid]):
                return {'error': 'Missing required parameters'}, 400
            
            success = CommentService.remove_comment_like(commentid, uid)
            return {'data': success}, 200
        except Exception as e:
            return {'error': str(e)}, 500

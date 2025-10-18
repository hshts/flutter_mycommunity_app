"""活动评论服务"""
from api import db
from api.models.comment import ActivityComment, ActivityCommentReply, ActivityCommentLike
from api.models.activity import Activity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid


class CommentService:
    """活动评论服务类"""
    
    @staticmethod
    def add_comment(data):
        """
        添加活动评论   
        Args:
            data: 评论数据
                - actid: 活动ID
                - uid: 用户ID
                - touid: 目标用户ID (可选)
                - content: 评论内容
                
        Returns:
            commentid: 评论ID
        """
        try:
            comment = ActivityComment(
                actid=data['actid'],
                uid=data['uid'],
                touid=data.get('touid'),
                content=data['content']
            )
            
            db.session.add(comment)
            
            # 更新活动评论数
            activity = Activity.query.get(data['actid'])
            if activity:
                activity.commentnum += 1
            
            db.session.commit()
            return comment.commentid
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def add_comment_reply(data):
        """
        添加评论回复
        
        Args:
            data: 回复数据
                - commentid: 评论ID
                - actid: 活动ID
                - uid: 用户ID
                - touid: 目标用户ID
                - content: 回复内容
                
        Returns:
            replyid: 回复ID
        """
        try:
            reply = ActivityCommentReply(
                commentid=data['commentid'],
                actid=data['actid'],
                uid=data['uid'],
                touid=data['touid'],
                content=data['content']
            )
            
            db.session.add(reply)
            
            # 更新评论回复数
            comment = ActivityComment.query.get(data['commentid'])
            if comment:
                comment.replynum += 1
            
            db.session.commit()
            return reply.replyid
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_comment_list(actid, uid=None):
        """
        获取活动评论列表
        
        Args:
            actid: 活动ID
            uid: 用户ID (用于判断是否点赞)
            
        Returns:
            评论列表
        """
        comments = ActivityComment.query.filter_by(
            actid=actid,
            status=1
        ).order_by(ActivityComment.createtime.desc()).all()
        
        result = []
        for comment in comments:
            comment_dict = comment.to_dict()
            
            # 添加用户信息（默认值）
            comment_dict['user'] = {
                'uid': comment.uid,
                'username': f'用户{comment.uid}',
                'profilepicture': 'https://via.placeholder.com/100'
            }
            
            # 如果有目标用户，添加目标用户信息
            if comment.touid:
                comment_dict['touser'] = {
                    'uid': comment.touid,
                    'username': f'用户{comment.touid}',
                    'profilepicture': 'https://via.placeholder.com/100'
                }
            
            # 如果提供了uid，检查是否点赞
            if uid:
                like = ActivityCommentLike.query.filter_by(
                    commentid=comment.commentid,
                    uid=uid
                ).first()
                comment_dict['isLiked'] = like is not None
            else:
                comment_dict['isLiked'] = False
            
            result.append(comment_dict)
        
        return result
    
    @staticmethod
    def get_reply_list(commentid):
        """
        获取评论回复列表
        
        Args:
            commentid: 评论ID
            
        Returns:
            回复列表
        """
        replies = ActivityCommentReply.query.filter_by(
            commentid=commentid,
            status=1
        ).order_by(ActivityCommentReply.createtime.asc()).all()
        
        result = []
        for reply in replies:
            reply_dict = reply.to_dict()
            
            # 添加用户信息
            reply_dict['user'] = {
                'uid': reply.uid,
                'username': f'用户{reply.uid}',
                'profilepicture': 'https://via.placeholder.com/100'
            }
            
            # 添加目标用户信息
            reply_dict['touser'] = {
                'uid': reply.touid,
                'username': f'用户{reply.touid}',
                'profilepicture': 'https://via.placeholder.com/100'
            }
            
            result.append(reply_dict)
        
        return result
    
    @staticmethod
    def get_reply(replyid):
        """
        获取指定回复
        
        Args:
            replyid: 回复ID
            
        Returns:
            回复对象
        """
        reply = ActivityCommentReply.query.get(replyid)
        if not reply:
            return None
        
        reply_dict = reply.to_dict()
        
        # 添加用户信息
        reply_dict['user'] = {
            'uid': reply.uid,
            'username': f'用户{reply.uid}',
            'profilepicture': 'https://via.placeholder.com/100'
        }
        
        # 添加目标用户信息
        reply_dict['touser'] = {
            'uid': reply.touid,
            'username': f'用户{reply.touid}',
            'profilepicture': 'https://via.placeholder.com/100'
        }
        
        return reply_dict
    
    @staticmethod
    def get_comment_reply_list(uid, replyid=None):
        """
        获取评论回复列表（用于获取用户相关的回复）
        
        Args:
            uid: 用户ID
            replyid: 回复ID (可选，用于获取特定回复之后的回复)
            
        Returns:
            回复列表
        """
        query = ActivityCommentReply.query.filter_by(
            touid=uid,
            status=1
        )
        
        if replyid:
            # 获取指定回复之后的回复
            target_reply = ActivityCommentReply.query.get(replyid)
            if target_reply:
                query = query.filter(
                    ActivityCommentReply.createtime > target_reply.createtime
                )
        
        replies = query.order_by(ActivityCommentReply.createtime.desc()).all()
        
        result = []
        for reply in replies:
            reply_dict = reply.to_dict()
            
            # 添加用户信息
            reply_dict['user'] = {
                'uid': reply.uid,
                'username': f'用户{reply.uid}',
                'profilepicture': 'https://via.placeholder.com/100'
            }
            
            # 添加活动信息
            activity = Activity.query.get(reply.actid)
            if activity:
                reply_dict['activity'] = {
                    'actid': activity.actid,
                    'content': activity.content[:50] if activity.content else '',
                    'coverimg': activity.coverimg
                }
            
            result.append(reply_dict)
        
        return result
    
    @staticmethod
    def get_new_comment_list(actid, commentid=None):
        """
        获取新评论列表（获取指定评论之后的评论和回复）
        
        Args:
            actid: 活动ID
            commentid: 评论ID (可选，获取此评论之后的新评论/回复)
            
        Returns:
            新评论和回复列表
        """
        result = []
        
        if commentid:
            # 获取指定评论的信息
            target_comment = ActivityComment.query.get(commentid)
            if not target_comment:
                return result
            
            # 获取该评论之后的新评论
            new_comments = ActivityComment.query.filter(
                ActivityComment.actid == actid,
                ActivityComment.createtime > target_comment.createtime,
                ActivityComment.status == 1
            ).order_by(ActivityComment.createtime.desc()).all()
            
            for comment in new_comments:
                comment_dict = comment.to_dict()
                comment_dict['type'] = 'comment'
                comment_dict['user'] = {
                    'uid': comment.uid,
                    'username': f'用户{comment.uid}',
                    'profilepicture': 'https://via.placeholder.com/100'
                }
                result.append(comment_dict)
            
            # 获取该评论的新回复
            new_replies = ActivityCommentReply.query.filter(
                ActivityCommentReply.commentid == commentid,
                ActivityCommentReply.createtime > target_comment.createtime,
                ActivityCommentReply.status == 1
            ).order_by(ActivityCommentReply.createtime.desc()).all()
            
            for reply in new_replies:
                reply_dict = reply.to_dict()
                reply_dict['type'] = 'reply'
                reply_dict['user'] = {
                    'uid': reply.uid,
                    'username': f'用户{reply.uid}',
                    'profilepicture': 'https://via.placeholder.com/100'
                }
                reply_dict['touser'] = {
                    'uid': reply.touid,
                    'username': f'用户{reply.touid}',
                    'profilepicture': 'https://via.placeholder.com/100'
                }
                result.append(reply_dict)
        else:
            # 如果没有指定commentid，返回所有评论
            comments = ActivityComment.query.filter_by(
                actid=actid,
                status=1
            ).order_by(ActivityComment.createtime.desc()).all()
            
            for comment in comments:
                comment_dict = comment.to_dict()
                comment_dict['type'] = 'comment'
                comment_dict['user'] = {
                    'uid': comment.uid,
                    'username': f'用户{comment.uid}',
                    'profilepicture': 'https://via.placeholder.com/100'
                }
                result.append(comment_dict)
        
        return result
    
    @staticmethod
    def add_comment_like(commentid, uid, likeuid, actid):
        """
        评论点赞
        
        Args:
            commentid: 评论ID
            uid: 点赞用户ID
            likeuid: 被点赞用户ID
            actid: 活动ID
            
        Returns:
            bool: 是否成功
        """
        try:
            # 检查是否已经点赞
            existing_like = ActivityCommentLike.query.filter_by(
                commentid=commentid,
                uid=uid
            ).first()
            
            if existing_like:
                return False  # 已经点赞过了
            
            # 添加点赞记录 (ActivityCommentLike只需要commentid和uid两个字段)
            like = ActivityCommentLike(
                commentid=commentid,
                uid=uid
            )
            db.session.add(like)
            
            # 更新评论点赞数
            comment = ActivityComment.query.get(commentid)
            if comment:
                comment.likenum += 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def remove_comment_like(commentid, uid):
        """
        取消评论点赞
        
        Args:
            commentid: 评论ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            # 查找点赞记录
            like = ActivityCommentLike.query.filter_by(
                commentid=commentid,
                uid=uid
            ).first()
            
            if not like:
                return False  # 没有点赞记录
            
            # 删除点赞记录
            db.session.delete(like)
            
            # 更新评论点赞数
            comment = ActivityComment.query.get(commentid)
            if comment:
                comment.likenum = max(0, comment.likenum - 1)
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_comment(commentid, uid):
        """
        删除评论
        
        Args:
            commentid: 评论ID
            uid: 用户ID (用于验证权限)
            
        Returns:
            bool: 是否成功
        """
        try:
            comment = ActivityComment.query.get(commentid)
            if not comment or comment.uid != uid:
                return False
            
            # 软删除
            comment.status = 0
            
            # 更新活动评论数
            activity = Activity.query.get(comment.actid)
            if activity:
                activity.commentnum = max(0, activity.commentnum - 1)
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_reply(replyid, uid):
        """
        删除回复
        
        Args:
            replyid: 回复ID
            uid: 用户ID (用于验证权限)
            
        Returns:
            bool: 是否成功
        """
        try:
            reply = ActivityCommentReply.query.get(replyid)
            if not reply or reply.uid != uid:
                return False
            
            # 软删除
            reply.status = 0
            
            # 更新评论回复数
            comment = ActivityComment.query.get(reply.commentid)
            if comment:
                comment.replynum = max(0, comment.replynum - 1)
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

"""动态(Moment)服务"""
from api import db
from api.models.moment import (
    Moment, MomentComment, MomentCommentReply, 
    MomentLike, MomentCommentLike
)
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class MomentService:
    """动态服务类"""
    
    @staticmethod
    def create_moment(uid, content, voice=None, images=None, coverimgwh=None, category=None):
        """
        发布动态
        
        Args:
            uid: 用户ID
            content: 动态内容
            voice: 音频文件路径
            images: 图片列表(JSON字符串)
            coverimgwh: 封面图宽高比
            category: 分类/话题
            
        Returns:
            momentid: 动态ID
        """
        try:
            moment = Moment(
                uid=uid,
                content=content,
                voice=voice,
                images=images,
                coverimgwh=coverimgwh,
                category=category
            )
            db.session.add(moment)
            db.session.commit()
            return moment.momentid
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_moment(momentid, uid):
        """
        删除动态
        
        Args:
            momentid: 动态ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            moment = Moment.query.filter_by(momentid=momentid, uid=uid).first()
            if not moment:
                return False
            
            moment.status = 0  # 软删除
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_moment_list(currentIndex=0, pagesize=20, subject=None):
        """
        获取动态列表
        
        Args:
            currentIndex: 当前索引(页码)
            pagesize: 每页数量
            subject: 主题/话题筛选
            
        Returns:
            list: 动态列表
        """
        try:
            query = Moment.query.filter_by(status=1)
            
            # 按话题筛选
            if subject:
                query = query.filter(Moment.category.like(f'%{subject}%'))
            
            # 按创建时间倒序
            query = query.order_by(Moment.createtime.desc())
            
            # 分页
            offset = currentIndex * pagesize
            moments = query.offset(offset).limit(pagesize).all()
            
            return [moment.to_dict() for moment in moments]
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def get_moment_info(momentid):
        """
        获取动态详情
        
        Args:
            momentid: 动态ID
            
        Returns:
            dict: 动态信息
        """
        try:
            moment = Moment.query.filter_by(momentid=momentid, status=1).first()
            return moment.to_dict() if moment else None
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def get_moment_list_by_user(uid, currentIndex=0, pagesize=20):
        """
        获取用户动态列表
        
        Args:
            uid: 用户ID
            currentIndex: 当前索引
            pagesize: 每页数量
            
        Returns:
            list: 动态列表
        """
        try:
            query = Moment.query.filter_by(uid=uid, status=1)
            query = query.order_by(Moment.createtime.desc())
            
            offset = currentIndex * pagesize
            moments = query.offset(offset).limit(pagesize).all()
            
            return [moment.to_dict() for moment in moments]
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def search_moment(content, currentIndex=0, pagesize=20):
        """
        搜索动态
        
        Args:
            content: 搜索内容
            currentIndex: 当前索引
            pagesize: 每页数量
            
        Returns:
            list: 动态列表
        """
        try:
            query = Moment.query.filter_by(status=1)
            
            # 搜索内容或分类
            if content:
                query = query.filter(
                    db.or_(
                        Moment.content.like(f'%{content}%'),
                        Moment.category.like(f'%{content}%')
                    )
                )
            
            query = query.order_by(Moment.createtime.desc())
            
            offset = currentIndex * pagesize
            moments = query.offset(offset).limit(pagesize).all()
            
            return [moment.to_dict() for moment in moments]
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def add_moment_like(momentid, uid):
        """
        动态点赞
        
        Args:
            momentid: 动态ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            # 检查是否已点赞
            existing_like = MomentLike.query.filter_by(
                momentid=momentid,
                uid=uid
            ).first()
            
            if existing_like:
                return False  # 已经点赞过了
            
            # 添加点赞记录
            like = MomentLike(
                momentid=momentid,
                uid=uid
            )
            db.session.add(like)
            
            # 更新动态点赞数
            moment = Moment.query.get(momentid)
            if moment:
                moment.likenum += 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def remove_moment_like(momentid, uid):
        """
        取消动态点赞
        
        Args:
            momentid: 动态ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            like = MomentLike.query.filter_by(
                momentid=momentid,
                uid=uid
            ).first()
            
            if not like:
                return False
            
            db.session.delete(like)
            
            # 更新动态点赞数
            moment = Moment.query.get(momentid)
            if moment and moment.likenum > 0:
                moment.likenum -= 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def add_moment_comment(momentid, uid, touid, content, commentid=None):
        """
        发布动态评论
        
        Args:
            momentid: 动态ID
            uid: 评论用户ID
            touid: 目标用户ID(评论时可为None,回复时必填)
            content: 评论内容
            commentid: 父评论ID(回复时使用)
            
        Returns:
            int: 评论ID或回复ID
        """
        try:
            if commentid:
                # 回复评论
                reply = MomentCommentReply(
                    commentid=commentid,
                    momentid=momentid,
                    uid=uid,
                    touid=touid,
                    content=content
                )
                db.session.add(reply)
                
                # 更新评论回复数
                comment = MomentComment.query.get(commentid)
                if comment:
                    comment.replynum += 1
                
                db.session.commit()
                return reply.replyid
            else:
                # 发布评论
                comment = MomentComment(
                    momentid=momentid,
                    uid=uid,
                    touid=touid,
                    content=content
                )
                db.session.add(comment)
                
                # 更新动态评论数
                moment = Moment.query.get(momentid)
                if moment:
                    moment.commentnum += 1
                
                db.session.commit()
                return comment.commentid
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_moment_comment(commentid, uid, replyid=None, momentid=None):
        """
        删除动态评论
        
        Args:
            commentid: 评论ID
            uid: 用户ID
            replyid: 回复ID(删除回复时使用)
            momentid: 动态ID
            
        Returns:
            bool: 是否成功
        """
        try:
            if replyid:
                # 删除回复
                reply = MomentCommentReply.query.filter_by(
                    replyid=replyid,
                    uid=uid
                ).first()
                
                if not reply:
                    return False
                
                reply.status = 0  # 软删除
                
                # 更新评论回复数
                comment = MomentComment.query.get(reply.commentid)
                if comment and comment.replynum > 0:
                    comment.replynum -= 1
            else:
                # 删除评论
                comment = MomentComment.query.filter_by(
                    commentid=commentid,
                    uid=uid
                ).first()
                
                if not comment:
                    return False
                
                comment.status = 0  # 软删除
                
                # 更新动态评论数
                if momentid:
                    moment = Moment.query.get(momentid)
                    if moment and moment.commentnum > 0:
                        moment.commentnum -= 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_moment_comment_list(momentid):
        """
        获取动态评论列表
        
        Args:
            momentid: 动态ID
            
        Returns:
            list: 评论列表
        """
        try:
            comments = MomentComment.query.filter_by(
                momentid=momentid,
                status=1
            ).order_by(MomentComment.createtime.desc()).all()
            
            return [comment.to_dict() for comment in comments]
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def add_moment_comment_like(commentid, uid):
        """
        动态评论点赞
        
        Args:
            commentid: 评论ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            # 检查是否已点赞
            existing_like = MomentCommentLike.query.filter_by(
                commentid=commentid,
                uid=uid
            ).first()
            
            if existing_like:
                return False
            
            # 添加点赞记录
            like = MomentCommentLike(
                commentid=commentid,
                uid=uid
            )
            db.session.add(like)
            
            # 更新评论点赞数
            comment = MomentComment.query.get(commentid)
            if comment:
                comment.likenum += 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def remove_moment_comment_like(commentid, uid):
        """
        取消动态评论点赞
        
        Args:
            commentid: 评论ID
            uid: 用户ID
            
        Returns:
            bool: 是否成功
        """
        try:
            like = MomentCommentLike.query.filter_by(
                commentid=commentid,
                uid=uid
            ).first()
            
            if not like:
                return False
            
            db.session.delete(like)
            
            # 更新评论点赞数
            comment = MomentComment.query.get(commentid)
            if comment and comment.likenum > 0:
                comment.likenum -= 1
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

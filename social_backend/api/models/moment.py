"""动态(Moment)模型"""
from api import db
from datetime import datetime


class Moment(db.Model):
    """动态模型"""
    __tablename__ = 'moments'
    
    momentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    voice = db.Column(db.String(500))  # 音频文件路径
    images = db.Column(db.Text)  # 图片列表,JSON格式存储
    coverimgwh = db.Column(db.String(50))  # 封面图宽高比
    category = db.Column(db.String(100))  # 分类/话题
    likenum = db.Column(db.Integer, default=0)  # 点赞数
    commentnum = db.Column(db.Integer, default=0)  # 评论数
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1: 正常, 0: 已删除
    
    def to_dict(self):
        """转换为字典"""
        return {
            'momentid': self.momentid,
            'uid': self.uid,
            'content': self.content,
            'voice': self.voice,
            'images': self.images,
            'coverimgwh': self.coverimgwh,
            'category': self.category,
            'likenum': self.likenum,
            'commentnum': self.commentnum,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'updatetime': self.updatetime.isoformat() if self.updatetime else None,
            'status': self.status
        }


class MomentComment(db.Model):
    """动态评论模型"""
    __tablename__ = 'moment_comments'
    
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    momentid = db.Column(db.Integer, nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False)
    touid = db.Column(db.Integer)  # 回复目标用户ID(评论时为空,回复时有值)
    content = db.Column(db.Text, nullable=False)
    likenum = db.Column(db.Integer, default=0)
    replynum = db.Column(db.Integer, default=0)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1: 正常, 0: 已删除
    
    def to_dict(self):
        """转换为字典"""
        return {
            'commentid': self.commentid,
            'momentid': self.momentid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'likenum': self.likenum,
            'replynum': self.replynum,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'status': self.status
        }


class MomentCommentReply(db.Model):
    """动态评论回复模型"""
    __tablename__ = 'moment_comment_replies'
    
    replyid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentid = db.Column(db.Integer, nullable=False, index=True)
    momentid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    touid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1: 正常, 0: 已删除
    
    def to_dict(self):
        """转换为字典"""
        return {
            'replyid': self.replyid,
            'commentid': self.commentid,
            'momentid': self.momentid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'status': self.status
        }


class MomentLike(db.Model):
    """动态点赞模型"""
    __tablename__ = 'moment_likes'
    
    likeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    momentid = db.Column(db.Integer, nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('momentid', 'uid', name='uq_moment_user_like'),
    )


class MomentCommentLike(db.Model):
    """动态评论点赞模型"""
    __tablename__ = 'moment_comment_likes'
    
    likeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentid = db.Column(db.Integer, nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('commentid', 'uid', name='uq_moment_comment_user_like'),
    )

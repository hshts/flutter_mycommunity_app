"""评论模型"""
from api import db
from datetime import datetime


class ActivityComment(db.Model):
    """活动评论模型"""
    __tablename__ = 'activity_comments'
    
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actid = db.Column(db.String(50), nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False)
    touid = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    likenum = db.Column(db.Integer, default=0)
    replynum = db.Column(db.Integer, default=0)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1: 正常, 0: 已删除
    
    def to_dict(self):
        """转换为字典"""
        return {
            'commentid': self.commentid,
            'actid': self.actid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'likenum': self.likenum,
            'replynum': self.replynum,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'status': self.status
        }


class ActivityCommentReply(db.Model):
    """活动评论回复模型"""
    __tablename__ = 'activity_comment_replies'
    
    replyid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentid = db.Column(db.Integer, nullable=False, index=True)
    actid = db.Column(db.String(50), nullable=False)
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
            'actid': self.actid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'status': self.status
        }


class ActivityCommentLike(db.Model):
    """活动评论点赞模型"""
    __tablename__ = 'activity_comment_likes'
    
    likeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentid = db.Column(db.Integer, nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('commentid', 'uid', name='uq_comment_user_like'),
    )

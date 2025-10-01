# 导入所有模型类
from .good_price import GoodPrice
from .comment import Comment
from .activity import Activity
from .user import User
from .collection import Collection, Like

__all__ = ['GoodPrice', 'Comment', 'Activity', 'User', 'Collection', 'Like']
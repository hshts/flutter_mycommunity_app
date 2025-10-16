from api import db
from api.models.activity import Activity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid

class ActivityService:
    @staticmethod
    def create_activity(data):
        """
        创建活动
        """
        try:
            # 如果没有提供actid，自动生成一个
            actid = data.get('actid') or f"act_{uuid.uuid4().hex[:16]}"
            
            activity = Activity(
                actid=actid,
                content=data.get('content'),
                uid=data.get('uid'),
                actprovince=data.get('province'),
                actcity=data.get('city'),
                address=data.get('address'),
                addresstitle=data.get('addresstitle'),
                lat=data.get('lat'),
                lng=data.get('lng'),
                coverimg=data.get('coverimg'),
                coverimgwh=data.get('coverimgWH'),
                startyear=data.get('startyear'),
                endyear=data.get('endyear'),
                paytype=data.get('paytype', 0),
                goodpriceid=data.get('goodpriceid')
            )
            
            db.session.add(activity)
            db.session.commit()
            return activity
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_activity_by_id(actid):
        """
        根据ID获取活动
        """
        if not actid:
            return []
        activity = Activity.query.get(actid)
        activity_dict = activity.to_dict()
             # 添加用户信息（默认值）
        activity_dict['user'] = {
                'uid': activity.uid,
                'username': f'用户{activity.uid}',
                'profilepicture': 'https://tse2.mm.bing.net/th/id/OIP.8E05GBXPjRW5vMtj-jO8ogHaE_?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3',
                'usertype': 1
               }

        return activity_dict

    @staticmethod
    def get_activities_by_update_time(current_index=0, citycode=None, page_size=20):
        """
        根据更新时间获取活动列表
        """
        query = Activity.query
        
        # 根据城市筛选
        if citycode:
            query = query.filter_by(actcity=citycode)
            
        # 分页查询
        activities = query.order_by(Activity.updatetime.desc())\
                         .offset(current_index)\
                         .limit(page_size)\
                         .all()
                # 为每个活动添加用户信息
        result = []
        for activity in activities:
            activity_dict = activity.to_dict()
             # 添加用户信息（默认值）
            activity_dict['user'] = {
                'uid': activity.uid,
                'username': f'用户{activity.uid}',
                'profilepicture': 'https://tse2.mm.bing.net/th/id/OIP.8E05GBXPjRW5vMtj-jO8ogHaE_?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3',
                'usertype': 1
            }
            result.append(activity_dict)

        return result

    @staticmethod
    def get_activities_by_user(current_index=0, uid=None, page_size=20):
        """
        根据用户获取活动列表
        """
        if not uid:
            return []
        
        activities = Activity.query\
                           .filter_by(uid=uid)\
                           .order_by(Activity.createtime.desc())\
                           .offset(current_index)\
                           .limit(page_size)\
                           .all()      
        return activities

    @staticmethod
    def get_activities_by_city(citycode, current_index=0, page_size=20, order_by='updatetime'):
        """
        根据城市获取活动列表
        
        Args:
            citycode: 城市代码
            current_index: 分页起始索引
            page_size: 每页数量
            order_by: 排序字段，可选 'updatetime', 'createtime', 'likenum', 'viewnum'
        
        Returns:
            活动列表
        """
        query = Activity.query.filter_by(status=1)  # 只获取状态为1的活动
        if citycode:
            query = query.filter_by(actcity=citycode)
        

        
        # 根据排序字段排序
        if order_by == 'createtime':
            query = query.order_by(Activity.createtime.desc())
        elif order_by == 'likenum':
            query = query.order_by(Activity.likenum.desc())
        elif order_by == 'viewnum':
            query = query.order_by(Activity.viewnum.desc())
        else:  # 默认按更新时间
            query = query.order_by(Activity.updatetime.desc())
        
        # 分页查询
        activities = query.offset(current_index)\
                         .limit(page_size)\
                         .all()
        # 为每个活动添加用户信息
        result = []
        for activity in activities:
            activity_dict = activity.to_dict()
             # 添加用户信息（默认值）
            activity_dict['user'] = {
                'uid': activity.uid,
                'username': f'用户{activity.uid}',
                'profilepicture': 'https://tse2.mm.bing.net/th/id/OIP.8E05GBXPjRW5vMtj-jO8ogHaE_?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3',
                'usertype': 1
            }
            result.append(activity_dict)

        return result

    @staticmethod
    def get_join_activities_by_user(current_index=0, uid=None, page_size=20):
        """
        获取用户参与的活动列表
        """
        if not uid:
            return []
        
        # 查询用户参与的活动（这里简化处理，实际应该有一个关联表）
        activities = Activity.query\
                           .filter(Activity.uid != uid)\
                           .filter(Activity.currentpeoplenum > 1)\
                           .order_by(Activity.createtime.desc())\
                           .offset(current_index)\
                           .limit(page_size)\
                           .all()
        return activities

    @staticmethod
    def update_like(actid, uid):
        """
        活动点赞
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新点赞数
        activity.likenum += 1
        db.session.commit()
        return activity

    @staticmethod
    def del_like(actid, uid):
        """
        活动取消点赞
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新点赞数（减少）
        activity.likenum = max(0, activity.likenum - 1)
        db.session.commit()
        return activity

    @staticmethod
    def update_collection(actid, uid):
        """
        活动收藏
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新收藏数
        activity.collectionnum += 1
        db.session.commit()
        return activity

    @staticmethod
    def del_collection(actid, uid):
        """
        活动取消收藏
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新收藏数（减少）
        activity.collectionnum = max(0, activity.collectionnum - 1)
        db.session.commit()
        return activity

    @staticmethod
    def update_comment(actid, uid, content):
        """
        发布活动评论
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新评论数
        activity.commentnum += 1
        db.session.commit()
        return activity

    @staticmethod
    def del_comment(actid, uid, commentid):
        """
        删除活动评论
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新评论数（减少）
        activity.commentnum = max(0, activity.commentnum - 1)
        db.session.commit()
        return activity

    @staticmethod
    def join_activity(actid, uid):
        """
        参加活动
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新参与人数
        activity.currentpeoplenum += 1
        activity.joinnum += 1
        db.session.commit()
        return activity

    @staticmethod
    def del_activity(actid, uid):
        """
        删除活动
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 删除活动
        db.session.delete(activity)
        db.session.commit()
        return True

    @staticmethod
    def update_activity_time(actid, uid, startyear, endyear):
        """
        更新活动时间
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新活动时间
        activity.startyear = startyear
        activity.endyear = endyear
        db.session.commit()
        return activity

    @staticmethod
    def update_activity(actid, uid, content, **kwargs):
        """
        更新活动信息
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新活动信息
        activity.content = content
        activity.address = kwargs.get('address')
        activity.addresstitle = kwargs.get('addresstitle')
        activity.lat = kwargs.get('lat')
        activity.lng = kwargs.get('lng')
        activity.coverimg = kwargs.get('coverimg')
        activity.coverimgwh = kwargs.get('coverimgwh')
        activity.actimagespath = kwargs.get('actimagespath')
        db.session.commit()
        return activity

    @staticmethod
    def update_activity_status(actid, uid, status):
        """
        更新活动状态
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新活动状态
        activity.status = status
        db.session.commit()
        return activity

    @staticmethod
    def exit_activity(actid, uid):
        """
        退出活动
        """
        activity = Activity.query.get(actid)
        if not activity:
            return None
        
        # 更新参与人数（减少）
        activity.currentpeoplenum = max(1, activity.currentpeoplenum - 1)
        activity.joinnum = max(0, activity.joinnum - 1)
        db.session.commit()
        return activity

    @staticmethod
    def get_group_conversation(timeline_id, uid):
        """
        获取群聊信息
        """
        activity = Activity.query.get(timeline_id)
        if not activity:
            return None
        
        # 返回群聊关系信息
        group_relation = {
            'timeline_id': activity.actid,
            'uid': uid,
            'name': f"活动群聊: {activity.content[:20]}",
            'group_name1': activity.content[:20]
        }
        
        return group_relation
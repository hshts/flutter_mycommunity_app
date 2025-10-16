import json
import pytest
from api import db
from api.models.activity import Activity
from tests.factories import ActivityFactory

class TestActivity:
    """Activity模块测试类"""
    
    def test_create_activity(self, client):
        """测试创建活动接口"""
        # 准备测试数据
        data = {
            "content": "测试活动内容",
            "uid": 1001,
            "province": "广东省",
            "city": "深圳市",
            "address": "深圳市南山区科技园",
            "addresstitle": "科技园",
            "lat": 22.5431,
            "lng": 113.9434,
            "coverimg": "https://example.com/cover.jpg",
            "coverimgWH": "640x480",
            "startyear": 1672502400,
            "endyear": 1672509600,
            "paytype": 0,
            "goodpriceid": "gp123456"
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/createActivity',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'content' in response_data
        assert response_data['content'] == data['content']
        assert response_data['uid'] == data['uid']
    
    def test_get_activity(self, client):
        """测试获取活动详情接口"""
        # 创建测试活动
        activity = ActivityFactory()
        
        # 发送GET请求
        response = client.get(f'/Activity/getActivity?actid={activity.actid}')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'actid' in response_data
        assert response_data['actid'] == activity.actid
        assert response_data['content'] == activity.content
    
    def test_get_activity_not_found(self, client):
        """测试获取不存在的活动"""
        # 发送GET请求
        response = client.get('/Activity/getActivity?actid=nonexistent')
        
        # 验证响应
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert 'error' in response_data
    
    def test_get_activities_by_update_time(self, client):
        """测试根据更新时间获取活动列表"""
        # 创建多个测试活动
        activities = ActivityFactory.create_batch(3)
        
        # 发送GET请求
        response = client.get('/Activity/getActivityListByUpdateTime')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert isinstance(response_data, list)
        assert len(response_data) == 3
    
    def test_get_activities_by_user(self, client):
        """测试根据用户获取活动列表"""
        # 创建测试活动
        uid = 1001
        ActivityFactory(uid=uid)
        ActivityFactory(uid=uid)
        ActivityFactory()  # 其他用户的活动
        
        # 发送GET请求
        response = client.get(f'/Activity/getActivityListByUser?uid={uid}')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert isinstance(response_data, list)
        assert len(response_data) == 2
        for activity in response_data:
            assert activity['uid'] == uid
    
    def test_get_join_activities_by_user(self, client):
        """测试获取用户参与的活动列表"""
        # 创建测试活动
        uid = 1001
        activity1 = ActivityFactory(uid=2001, currentpeoplenum=5)  # 其他用户创建的活动
        activity2 = ActivityFactory(uid=2002, currentpeoplenum=3)  # 其他用户创建的活动
        ActivityFactory(uid=uid)  # 当前用户创建的活动（不包含在结果中）
        
        # 发送GET请求
        response = client.get(f'/Activity/getJoinActivityListByUser?uid={uid}')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert isinstance(response_data, list)
        # 应该返回其他用户创建且有人参与的活动
        assert len(response_data) == 2
    
    def test_get_activities_by_city(self, client):
        """测试根据城市获取活动列表"""
        # 创建测试活动
        citycode = "440300"  # 深圳市代码
        ActivityFactory(actcity=citycode, likenum=10)
        ActivityFactory(actcity=citycode, likenum=5)
        ActivityFactory(actcity="110100")  # 北京市，不应包含在结果中
        
        # 发送GET请求
        response = client.get(f'/Activity/getActivityListByCity?citycode={citycode}')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert 'citycode' in response_data
        assert response_data['citycode'] == citycode
        assert len(response_data['data']) == 2
        
        # 验证所有活动都属于指定城市
        for activity in response_data['data']:
            assert activity['actcity'] == citycode
    
    def test_get_activities_by_city_with_order(self, client):
        """测试根据城市获取活动列表（带排序）"""
        # 创建测试活动
        citycode = "440300"
        ActivityFactory(actcity=citycode, likenum=5)
        ActivityFactory(actcity=citycode, likenum=10)
        ActivityFactory(actcity=citycode, likenum=3)
        
        # 按点赞数排序
        response = client.get(f'/Activity/getActivityListByCity?citycode={citycode}&orderBy=likenum')
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert len(response_data['data']) == 3
        
        # 验证是否按点赞数降序排列
        like_nums = [activity['likenum'] for activity in response_data['data']]
        assert like_nums == sorted(like_nums, reverse=True)
    
    def test_get_activities_by_city_missing_citycode(self, client):
        """测试根据城市获取活动列表（缺少citycode参数）"""
        # 发送GET请求，不提供citycode
        response = client.get('/Activity/getActivityListByCity')
        
        # 验证响应
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
    
    def test_update_like(self, client):
        """测试活动点赞"""
        # 创建测试活动
        activity = ActivityFactory(likenum=5)
        original_like_count = activity.likenum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updateLike',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.likenum == original_like_count + 1
    
    def test_del_like(self, client):
        """测试活动取消点赞"""
        # 创建测试活动
        activity = ActivityFactory(likenum=5)
        original_like_count = activity.likenum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/delLike',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.likenum == original_like_count - 1
    
    def test_update_collection(self, client):
        """测试活动收藏"""
        # 创建测试活动
        activity = ActivityFactory(collectionnum=3)
        original_collection_count = activity.collectionnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updateCollection',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.collectionnum == original_collection_count + 1
    
    def test_del_collection(self, client):
        """测试活动取消收藏"""
        # 创建测试活动
        activity = ActivityFactory(collectionnum=3)
        original_collection_count = activity.collectionnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/delCollection',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.collectionnum == original_collection_count - 1
    
    def test_update_comment(self, client):
        """测试发布活动评论"""
        # 创建测试活动
        activity = ActivityFactory(commentnum=2)
        original_comment_count = activity.commentnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001,
            "content": "测试评论内容"
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updatecomment',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert isinstance(response_data['data'], int)
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.commentnum == original_comment_count + 1
    
    def test_del_comment(self, client):
        """测试删除活动评论"""
        # 创建测试活动
        activity = ActivityFactory(commentnum=5)
        original_comment_count = activity.commentnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001,
            "commentid": 123
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/delcomment',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.commentnum == original_comment_count - 1
    
    def test_join_activity(self, client):
        """测试参加活动"""
        # 创建测试活动
        activity = ActivityFactory(currentpeoplenum=3, joinnum=2)
        original_people_count = activity.currentpeoplenum
        original_join_count = activity.joinnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/joinActivity',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data']['timeline_id'] == activity.actid
        assert response_data['data']['uid'] == data['uid']
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.currentpeoplenum == original_people_count + 1
        assert updated_activity.joinnum == original_join_count + 1
    
    def test_del_activity(self, client):
        """测试删除活动"""
        # 创建测试活动
        activity = ActivityFactory()
        actid = activity.actid
        
        # 确保活动存在
        assert Activity.query.get(actid) is not None
        
        # 准备测试数据
        data = {
            "actid": actid,
            "uid": activity.uid
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/delActivity',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        assert Activity.query.get(actid) is None
    
    def test_update_activity_time(self, client):
        """测试更新活动时间"""
        # 创建测试活动
        activity = ActivityFactory()
        new_start_time = 1672588800
        new_end_time = 1672596000
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": activity.uid,
            "startyear": new_start_time,
            "endyear": new_end_time
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updateActivityTime',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.startyear == new_start_time
        assert updated_activity.endyear == new_end_time
    
    def test_update_activity(self, client):
        """测试更新活动信息"""
        # 创建测试活动
        activity = ActivityFactory()
        new_content = "更新后的活动内容"
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": activity.uid,
            "content": new_content,
            "address": "新地址",
            "addresstitle": "新地址标题"
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updateActivity',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.content == new_content
        assert updated_activity.address == "新地址"
        assert updated_activity.addresstitle == "新地址标题"
    
    def test_update_activity_status(self, client):
        """测试更新活动状态"""
        # 创建测试活动
        activity = ActivityFactory(status=1)
        new_status = 2
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": activity.uid,
            "status": new_status
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/updateActivityStatus',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] is True
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.status == new_status
    
    def test_exit_activity(self, client):
        """测试退出活动"""
        # 创建测试活动
        activity = ActivityFactory(currentpeoplenum=5, joinnum=4)
        original_people_count = activity.currentpeoplenum
        original_join_count = activity.joinnum
        
        # 准备测试数据
        data = {
            "actid": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/exitActivity',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data'] == 1
        
        # 验证数据库更新
        updated_activity = Activity.query.get(activity.actid)
        assert updated_activity.currentpeoplenum == original_people_count - 1
        assert updated_activity.joinnum == original_join_count - 1
    
    def test_get_group_conversation(self, client):
        """测试获取群聊信息"""
        # 创建测试活动
        activity = ActivityFactory()
        
        # 准备测试数据
        data = {
            "timeline_id": activity.actid,
            "uid": 1001
        }
        
        # 发送POST请求
        response = client.post(
            '/Activity/getGroupConversation',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # 验证响应
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'data' in response_data
        assert response_data['data']['timeline_id'] == activity.actid
        assert response_data['data']['uid'] == data['uid']
        assert 'name' in response_data['data']
        assert 'group_name1' in response_data['data']
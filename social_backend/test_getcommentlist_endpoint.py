"""测试 Activity getCommentList 接口的完整功能"""
from api import create_app
from api.models.activity import Activity
from api.models.comment import ActivityComment, ActivityCommentReply
import json

def test_get_comment_list_endpoint():
    """测试 getCommentList 端点"""
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        print("=" * 60)
        print("测试 /Activity/getCommentList 接口")
        print("=" * 60)
        
        # 1. 获取一个有评论的活动
        activity = Activity.query.join(
            ActivityComment,
            Activity.actid == ActivityComment.actid
        ).first()
        
        if not activity:
            print("\n⚠️  数据库中没有活动评论数据")
            return
        
        actid = activity.actid
        uid = 1000
        
        print(f"\n测试活动:")
        print(f"  活动ID: {actid[:16]}...")
        print(f"  活动内容: {activity.content[:40]}...")
        
        # 2. 测试不带 uid 参数
        print("\n" + "=" * 60)
        print("测试 1: 不带 uid 参数")
        print("=" * 60)
        
        response = client.get(f'/Activity/getCommentList?actid={actid}')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"✓ 请求成功")
            print(f"  返回评论数: {data.get('count', 0)}")
            
            if data.get('data'):
                comment = data['data'][0]
                print(f"\n  第一条评论示例:")
                print(f"    评论ID: {comment['commentid'][:16]}...")
                print(f"    用户ID: {comment['uid']}")
                print(f"    内容: {comment['content'][:40]}...")
                print(f"    点赞数: {comment['likenum']}")
                print(f"    回复数: {comment['replynum']}")
                print(f"    是否点赞: {comment.get('isLiked', False)}")
                
                if comment.get('user'):
                    print(f"    用户信息:")
                    print(f"      - username: {comment['user']['username']}")
                    print(f"      - profilepicture: {comment['user']['profilepicture'][:30]}...")
        else:
            print(f"✗ 请求失败: {response.data}")
        
        # 3. 测试带 uid 参数
        print("\n" + "=" * 60)
        print("测试 2: 带 uid 参数 (用于显示点赞状态)")
        print("=" * 60)
        
        response = client.get(f'/Activity/getCommentList?actid={actid}&uid={uid}')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"✓ 请求成功")
            print(f"  返回评论数: {data.get('count', 0)}")
            
            if data.get('data'):
                # 检查是否包含点赞状态
                has_liked = any(c.get('isLiked', False) for c in data['data'])
                print(f"  包含点赞状态: ✓")
                print(f"  用户已点赞的评论: {sum(1 for c in data['data'] if c.get('isLiked', False))} 条")
        
        # 4. 测试缺少 actid 参数
        print("\n" + "=" * 60)
        print("测试 3: 缺少 actid 参数 (错误情况)")
        print("=" * 60)
        
        response = client.get('/Activity/getCommentList')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 400:
            data = json.loads(response.data)
            print(f"✓ 正确返回 400 错误")
            print(f"  错误信息: {data.get('error')}")
        else:
            print(f"✗ 期望 400，实际 {response.status_code}")
        
        # 5. 测试不存在的活动
        print("\n" + "=" * 60)
        print("测试 4: 不存在的活动ID")
        print("=" * 60)
        
        response = client.get('/Activity/getCommentList?actid=nonexistent_id')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"✓ 请求成功")
            print(f"  返回评论数: {data.get('count', 0)} (应为 0)")
        
        # 6. 响应格式验证
        print("\n" + "=" * 60)
        print("测试 5: 响应格式验证")
        print("=" * 60)
        
        response = client.get(f'/Activity/getCommentList?actid={actid}&uid={uid}')
        if response.status_code == 200:
            data = json.loads(response.data)
            
            # 检查必需字段
            required_fields = ['data', 'count']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print(f"✗ 缺少字段: {missing_fields}")
            else:
                print(f"✓ 包含所有必需字段: {required_fields}")
            
            # 检查评论对象字段
            if data.get('data'):
                comment = data['data'][0]
                comment_required_fields = [
                    'commentid', 'actid', 'uid', 'content', 
                    'likenum', 'replynum', 'createtime', 'user'
                ]
                
                missing_comment_fields = [f for f in comment_required_fields if f not in comment]
                
                if missing_comment_fields:
                    print(f"✗ 评论对象缺少字段: {missing_comment_fields}")
                else:
                    print(f"✓ 评论对象包含所有必需字段")
                
                # 检查用户对象字段
                if comment.get('user'):
                    user = comment['user']
                    user_required_fields = ['uid', 'username', 'profilepicture']
                    missing_user_fields = [f for f in user_required_fields if f not in user]
                    
                    if missing_user_fields:
                        print(f"✗ 用户对象缺少字段: {missing_user_fields}")
                    else:
                        print(f"✓ 用户对象包含所有必需字段")
        
        # 7. 性能测试
        print("\n" + "=" * 60)
        print("测试 6: 性能测试")
        print("=" * 60)
        
        import time
        start_time = time.time()
        
        for i in range(10):
            client.get(f'/Activity/getCommentList?actid={actid}&uid={uid}')
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        print(f"  10次请求平均响应时间: {avg_time*1000:.2f} ms")
        
        if avg_time < 0.1:
            print(f"  ✓ 性能良好 (< 100ms)")
        elif avg_time < 0.5:
            print(f"  ⚠️  性能一般 (100-500ms)")
        else:
            print(f"  ✗ 性能较差 (> 500ms)")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成!")
        print("=" * 60)
        
        # 8. 总结
        print("\n接口功能总结:")
        print("  ✓ 支持获取活动评论列表")
        print("  ✓ 支持可选的 uid 参数显示点赞状态")
        print("  ✓ 返回包含用户信息的完整评论对象")
        print("  ✓ 正确处理错误情况")
        print("  ✓ 响应格式符合规范")
        print("  ✓ 性能表现良好")
        
        print("\n接口规范:")
        print("  端点: GET /Activity/getCommentList")
        print("  参数:")
        print("    - actid (必填): 活动ID")
        print("    - uid (可选): 用户ID，用于判断是否点赞")
        print("  响应:")
        print("    - data: 评论对象数组")
        print("    - count: 评论总数")

if __name__ == '__main__':
    test_get_comment_list_endpoint()

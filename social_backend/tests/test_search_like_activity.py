"""测试 searchMoreLikeActivity 接口"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_search_more_like_activity():
    """测试搜索更多类似活动接口"""
    print("=" * 70)
    print("🔍 测试 searchMoreLikeActivity 接口")
    print("=" * 70)
    
    url = f"{BASE_URL}/Activity/searchMoreLikeActivity"
    
    # 测试 1: 不带 actid 的基础搜索
    print("\n【测试 1】基础搜索（不指定活动ID）")
    print("-" * 70)
    
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "currIndex": 0,
        "pageSize": 10
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"📍 URL: {url}")
        print(f"📍 请求数据: {json.dumps(data, indent=2)}")
        print(f"📍 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ 请求成功!")
            print(f"   返回活动数量: {result.get('count', 0)}")
            print(f"   当前索引: {result.get('currIndex')}")
            print(f"   每页大小: {result.get('pageSize')}")
            
            if result.get('data') and len(result['data']) > 0:
                print(f"\n📋 前 3 个活动:")
                for i, activity in enumerate(result['data'][:3], 1):
                    print(f"\n   活动 {i}:")
                    print(f"     ID: {activity.get('actid')}")
                    print(f"     内容: {activity.get('content', '')[:50]}...")
                    print(f"     城市: {activity.get('actcity')}")
                    print(f"     点赞数: {activity.get('likenum')}")
                    print(f"     浏览数: {activity.get('viewnum')}")
                    print(f"     参与数: {activity.get('joinnum')}")
            else:
                print("\n⚠️  暂无活动数据")
        else:
            print(f"\n❌ 请求失败")
            print(f"   响应内容: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
    
    # 测试 2: 带 actid 的类似活动搜索
    print("\n" + "=" * 70)
    print("【测试 2】查找类似活动（指定活动ID）")
    print("-" * 70)
    
    # 先获取一个活动ID
    try:
        # 先调用获取活动列表接口
        list_url = f"{BASE_URL}/Activity/getActivityListByCity"
        params = {
            'citycode': 'all',
            'currentIndex': 0,
            'pageSize': 1
        }
        list_response = requests.get(list_url, params=params)
        
        if list_response.status_code == 200:
            list_result = list_response.json()
            if list_result.get('data') and len(list_result['data']) > 0:
                test_actid = list_result['data'][0].get('actid')
                print(f"📍 测试活动ID: {test_actid}")
                
                # 搜索类似活动
                data = {
                    "actid": test_actid,
                    "currIndex": 0,
                    "pageSize": 5
                }
                
                response = requests.post(url, json=data, headers=headers)
                print(f"📍 请求数据: {json.dumps(data, indent=2)}")
                print(f"📍 状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"\n✅ 请求成功!")
                    print(f"   返回类似活动数量: {result.get('count', 0)}")
                    
                    if result.get('data') and len(result['data']) > 0:
                        print(f"\n📋 类似活动列表:")
                        for i, activity in enumerate(result['data'], 1):
                            print(f"\n   类似活动 {i}:")
                            print(f"     ID: {activity.get('actid')}")
                            print(f"     内容: {activity.get('content', '')[:40]}...")
                            print(f"     城市: {activity.get('actcity')}")
                            print(f"     费用: {activity.get('mincost')}-{activity.get('maxcost')}")
                            print(f"     热度: {activity.get('likenum', 0) + activity.get('viewnum', 0) + activity.get('joinnum', 0)}")
                    else:
                        print("\n⚠️  没有找到类似活动")
                else:
                    print(f"\n❌ 请求失败")
                    print(f"   响应内容: {response.text[:200]}")
            else:
                print("\n⚠️  暂无活动数据，跳过类似活动测试")
        else:
            print("\n⚠️  无法获取活动列表，跳过类似活动测试")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
    
    # 测试 3: 分页测试
    print("\n" + "=" * 70)
    print("【测试 3】分页测试")
    print("-" * 70)
    
    data = {
        "currIndex": 0,
        "pageSize": 5
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            page1_count = result.get('count', 0)
            print(f"✅ 第一页: {page1_count} 个活动")
            
            # 获取第二页
            data['currIndex'] = 5
            response2 = requests.post(url, json=data, headers=headers)
            
            if response2.status_code == 200:
                result2 = response2.json()
                page2_count = result2.get('count', 0)
                print(f"✅ 第二页: {page2_count} 个活动")
                print(f"\n📊 分页功能正常")
            else:
                print(f"❌ 第二页请求失败")
        else:
            print(f"❌ 第一页请求失败")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎉 测试完成")
    print("=" * 70)

if __name__ == '__main__':
    test_search_more_like_activity()

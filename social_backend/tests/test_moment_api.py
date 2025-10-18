"""测试动态(Moment)相关API接口"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_moment_list():
    """测试获取动态列表"""
    print("\n" + "=" * 70)
    print("测试 1: 获取动态列表 (POST /IM/getMomentList)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/getMomentList"
    payload = {
        "currIndex": 0,
        "subject": "美食"
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            moments = data.get('data', {}).get('list', [])
            print(f"\n✅ 成功获取 {len(moments)} 条动态")
            if moments:
                print(f"\n第一条动态:")
                print(f"  - momentid: {moments[0].get('momentid')}")
                print(f"  - uid: {moments[0].get('uid')}")
                print(f"  - content: {moments[0].get('content')}")
                print(f"  - category: {moments[0].get('category')}")
                print(f"  - likenum: {moments[0].get('likenum')}")
                print(f"  - commentnum: {moments[0].get('commentnum')}")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器 (python3 run.py)")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def test_get_moment_info():
    """测试获取动态详情"""
    print("\n" + "=" * 70)
    print("测试 2: 获取动态详情 (POST /IM/getMomentInfo)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/getMomentInfo"
    payload = {
        "momentid": 1
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            print(f"\n✅ 成功获取动态详情")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def test_create_moment():
    """测试发布动态"""
    print("\n" + "=" * 70)
    print("测试 3: 发布动态 (POST /IM/reportMoment)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/reportMoment"
    payload = {
        "uid": 1005,
        "token": "test_token",
        "content": "这是一条测试动态,分享今天的好心情!",
        "category": "生活分享",
        "images": json.dumps([
            "https://example.com/test1.jpg",
            "https://example.com/test2.jpg"
        ]),
        "coverimgwh": "16:9"
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            momentid = data.get('data', {}).get('momentid')
            print(f"\n✅ 成功发布动态, momentid: {momentid}")
            return momentid
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
        return None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return None


def test_update_moment_like():
    """测试动态点赞"""
    print("\n" + "=" * 70)
    print("测试 4: 动态点赞 (POST /IM/updateMomentLike)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/updateMomentLike"
    payload = {
        "token": "test_token",
        "momentid": 2,
        "uid": 9999
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            print(f"\n✅ 点赞成功")
        elif data.get('code') == 201:
            print(f"\n⚠️  已经点赞过了")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def test_update_moment_comment():
    """测试发布动态评论"""
    print("\n" + "=" * 70)
    print("测试 5: 发布动态评论 (POST /IM/updateMomentComment)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/updateMomentComment"
    payload = {
        "token": "test_token",
        "momentid": 1,
        "uid": 9999,
        "content": "这是一条测试评论,内容很精彩!"
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            comment_id = data.get('data', {}).get('id')
            print(f"\n✅ 评论成功, commentid: {comment_id}")
            return comment_id
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
        return None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return None


def test_get_moment_comment():
    """测试获取动态评论列表"""
    print("\n" + "=" * 70)
    print("测试 6: 获取动态评论列表 (GET /IM/getMomentComment)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/getMomentComment"
    params = {
        "momentid": 1
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            comments = data.get('data', {}).get('list', [])
            print(f"\n✅ 成功获取 {len(comments)} 条评论")
            if comments:
                print(f"\n第一条评论:")
                print(f"  - commentid: {comments[0].get('commentid')}")
                print(f"  - uid: {comments[0].get('uid')}")
                print(f"  - content: {comments[0].get('content')}")
                print(f"  - likenum: {comments[0].get('likenum')}")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def test_search_moment():
    """测试搜索动态"""
    print("\n" + "=" * 70)
    print("测试 7: 搜索动态 (POST /IM/searchMoment)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/searchMoment"
    payload = {
        "content": "分享",
        "currentIndex": 0
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            moments = data.get('data', {}).get('list', [])
            print(f"\n✅ 搜索到 {len(moments)} 条动态")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def test_get_moment_list_by_user():
    """测试获取用户动态列表"""
    print("\n" + "=" * 70)
    print("测试 8: 获取用户动态列表 (POST /IM/getMomentListByUser)")
    print("=" * 70)
    
    url = f"{BASE_URL}/IM/getMomentListByUser"
    payload = {
        "uid": 1000
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if data.get('code') == 200:
            moments = data.get('data', {}).get('list', [])
            print(f"\n✅ 用户1000发布了 {len(moments)} 条动态")
        else:
            print(f"❌ 请求失败: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")


def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("动态(Moment)相关API接口测试")
    print("=" * 70)
    print("\n📝 测试说明:")
    print("  - 测试IM模块中关于moment的所有服务接口")
    print("  - 验证接口功能和数据正确性")
    print("\n⚠️  前提条件: Flask服务器需要在运行中 (python3 run.py)")
    
    # 运行测试
    test_get_moment_list()
    test_get_moment_info()
    test_create_moment()
    test_update_moment_like()
    test_update_moment_comment()
    test_get_moment_comment()
    test_search_moment()
    test_get_moment_list_by_user()
    
    print("\n" + "=" * 70)
    print("✅ 测试完成!")
    print("=" * 70)
    print("\n💡 如果看到连接错误,请先运行: python3 run.py")

if __name__ == '__main__':
    main()

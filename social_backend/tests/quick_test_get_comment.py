"""快速测试获取评论接口"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_get_moment_comment():
    """测试获取动态评论列表"""
    print("测试 GET /IM/getMomentComment")
    print("=" * 60)
    
    url = f"{BASE_URL}/IM/getMomentComment"
    params = {"momentid": 1}
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                comments = data.get('data', {}).get('list', [])
                print(f"\n✅ 成功获取 {len(comments)} 条评论")
                if comments:
                    print(f"第一条评论: commentid={comments[0].get('commentid')}, content={comments[0].get('content')}")
            else:
                print(f"❌ 接口返回错误: {data.get('msg')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")

if __name__ == '__main__':
    test_get_moment_comment()

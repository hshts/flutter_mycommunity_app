"""快速测试 GoodPrice 评论 API"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_comment_api():
    """测试评论 API"""
    print("=" * 70)
    print("🧪 测试 GoodPrice 评论 API")
    print("=" * 70)
    
    # 测试商品ID（从刚才的输出）
    test_goodpriceid = "7916215a-ed83-4ff8-af65-a51a210bede6"
    
    # 1. 获取评论列表
    print("\n【测试 1】获取评论列表 (GET)")
    print("-" * 70)
    url = f"{BASE_URL}/grouppurchase/getcomment"
    params = {
        "goodpriceid": test_goodpriceid,
        "uid": "1001"
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 请求成功")
            print(f"\n响应数据:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            comments = result.get('data', [])
            print(f"\n📊 评论统计:")
            print(f"   评论总数: {len(comments)}")
            
            if comments:
                first_comment = comments[0]
                commentid = first_comment.get('commentid')
                print(f"\n   第一条评论:")
                print(f"   - commentid: {commentid} (类型: {type(commentid).__name__})")
                
                if isinstance(commentid, int):
                    print(f"   ✅ commentid 是 Integer 类型!")
                else:
                    print(f"   ⚠️  commentid 不是 Integer 类型")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求出错: {str(e)}")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == '__main__':
    test_comment_api()

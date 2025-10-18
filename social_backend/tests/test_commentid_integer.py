"""测试 commentid 改为 Integer 后的功能"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_comment_with_integer_id():
    """测试使用 Integer commentid 的评论功能"""
    print("=" * 60)
    print("测试 GoodPriceComment 使用 Integer commentid")
    print("=" * 60)
    
    # 假设的测试数据
    test_goodpriceid = "test-product-001"
    test_uid = 1001
    test_token = "test-token"
    
    # 1. 创建评论
    print("\n【测试 1】创建评论")
    print("-" * 60)
    url = f"{BASE_URL}/grouppurchase/updatecomment"
    data = {
        "token": test_token,
        "goodpriceid": test_goodpriceid,
        "uid": test_uid,
        "content": "这是一条测试评论,commentid 现在是 Integer 类型"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and result.get('success'):
            commentid = result.get('commentid')
            print(f"✅ 评论创建成功")
            print(f"   commentid: {commentid}")
            print(f"   类型: {type(commentid).__name__}")
            
            if isinstance(commentid, int):
                print(f"   ✅ commentid 是 Integer 类型")
            else:
                print(f"   ⚠️  commentid 不是 Integer 类型: {type(commentid)}")
                
            # 2. 创建回复
            print("\n【测试 2】创建回复")
            print("-" * 60)
            reply_data = {
                "token": test_token,
                "commentid": commentid,  # 使用上面创建的 commentid
                "goodpriceid": test_goodpriceid,
                "uid": test_uid + 1,
                "touid": test_uid,
                "content": "这是一条回复"
            }
            
            response2 = requests.post(url, json=reply_data)
            print(f"状态码: {response2.status_code}")
            result2 = response2.json()
            print(f"响应: {json.dumps(result2, indent=2, ensure_ascii=False)}")
            
            if response2.status_code == 200 and result2.get('success'):
                print(f"✅ 回复创建成功")
            
            # 3. 获取评论列表
            print("\n【测试 3】获取评论列表")
            print("-" * 60)
            url_get = f"{BASE_URL}/grouppurchase/getcomment"
            params = {
                "goodpriceid": test_goodpriceid,
                "uid": test_uid
            }
            
            response3 = requests.get(url_get, params=params)
            print(f"状态码: {response3.status_code}")
            result3 = response3.json()
            print(f"响应: {json.dumps(result3, indent=2, ensure_ascii=False)}")
            
            if response3.status_code == 200:
                comments = result3.get('data', [])
                print(f"✅ 获取到 {len(comments)} 条评论")
                for comment in comments:
                    cid = comment.get('commentid')
                    print(f"   - commentid: {cid} (类型: {type(cid).__name__})")
            
            # 4. 点赞评论
            print("\n【测试 4】评论点赞")
            print("-" * 60)
            url_like = f"{BASE_URL}/grouppurchase/updateCommentLike"
            like_data = {
                "token": test_token,
                "commentid": commentid,  # Integer 类型
                "uid": test_uid + 2,
                "likeuid": test_uid,
                "goodpriceid": test_goodpriceid
            }
            
            response4 = requests.post(url_like, json=like_data)
            print(f"状态码: {response4.status_code}")
            result4 = response4.json()
            print(f"响应: {json.dumps(result4, indent=2, ensure_ascii=False)}")
            
            if response4.status_code == 200:
                print(f"✅ 评论点赞成功")
            
        else:
            print(f"❌ 创建评论失败")
            
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_comment_with_integer_id()

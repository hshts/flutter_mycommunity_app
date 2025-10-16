"""快速测试Integer类型commentid的API接口"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_comment_list():
    """测试获取评论列表接口"""
    print("\n" + "=" * 70)
    print("测试 1: 获取评论列表 (GET /Activity/getCommentList)")
    print("=" * 70)
    
    # 先获取一个actid
    url = f"{BASE_URL}/Activity/getCommentList"
    payload = {
        "actid": "ACT001",
        "uid": 1000,
        "pageindex": 1,
        "pagesize": 3
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('code') == 200:
            print("✅ 接口调用成功")
            comments = data.get('data', {}).get('list', [])
            print(f"✅ 返回 {len(comments)} 条评论")
            
            if comments:
                print("\n评论ID类型验证:")
                for comment in comments[:2]:
                    commentid = comment.get('commentid')
                    print(f"  - commentid: {commentid} (类型: {type(commentid).__name__})")
                    
                    # 验证是否为整数
                    if isinstance(commentid, int):
                        print(f"    ✅ 正确: Integer类型")
                    else:
                        print(f"    ❌ 错误: 应该是Integer,实际是{type(commentid).__name__}")
        else:
            print(f"❌ 接口返回错误: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器 (python3 run.py)")
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

def test_get_reply_list():
    """测试获取回复列表接口"""
    print("\n" + "=" * 70)
    print("测试 2: 获取回复列表 (GET /Activity/getReplyList)")
    print("=" * 70)
    
    url = f"{BASE_URL}/Activity/getReplyList"
    payload = {
        "commentid": 1,  # 使用Integer类型的commentid
        "uid": 1000,
        "pageindex": 1,
        "pagesize": 5
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('code') == 200:
            print("✅ 接口调用成功")
            replies = data.get('data', {}).get('list', [])
            print(f"✅ 评论ID={payload['commentid']} 有 {len(replies)} 条回复")
            
            if replies:
                print("\n回复ID类型验证:")
                for reply in replies[:2]:
                    replyid = reply.get('replyid')
                    commentid = reply.get('commentid')
                    print(f"  - replyid: {replyid} (类型: {type(replyid).__name__})")
                    print(f"    commentid: {commentid} (类型: {type(commentid).__name__})")
                    
                    if isinstance(replyid, int) and isinstance(commentid, int):
                        print(f"    ✅ 正确: 所有ID都是Integer类型")
                    else:
                        print(f"    ❌ 错误: ID应该都是Integer类型")
        else:
            print(f"❌ 接口返回错误: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器 (python3 run.py)")
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

def test_update_comment_like():
    """测试点赞接口"""
    print("\n" + "=" * 70)
    print("测试 3: 点赞评论 (POST /Activity/updateCommentLike)")
    print("=" * 70)
    
    url = f"{BASE_URL}/Activity/updateCommentLike"
    payload = {
        "commentid": 2,  # 使用Integer类型的commentid
        "uid": 9999,
        "actid": "ACT001"
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('code') == 200:
            print(f"✅ 点赞成功: commentid={payload['commentid']}")
            print(f"✅ 接口正确处理了Integer类型的commentid")
        elif data.get('code') == 201:
            print(f"⚠️  已经点赞过了: commentid={payload['commentid']}")
            print(f"✅ 接口正确处理了Integer类型的commentid")
        else:
            print(f"❌ 接口返回错误: {data.get('msg')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先启动Flask服务器 (python3 run.py)")
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("Integer类型 commentid API接口测试")
    print("=" * 70)
    print("\n📝 测试说明:")
    print("  1. 验证API接口能正确处理Integer类型的commentid")
    print("  2. 检查返回数据中的ID字段类型")
    print("  3. 确认外键关系正常工作")
    print("\n⚠️  前提条件: Flask服务器需要在运行中 (python3 run.py)")
    
    # 运行测试
    test_get_comment_list()
    test_get_reply_list()
    test_update_comment_like()
    
    print("\n" + "=" * 70)
    print("✅ 测试完成!")
    print("=" * 70)
    print("\n💡 如果看到连接错误,请先运行: python3 run.py")

if __name__ == '__main__':
    main()

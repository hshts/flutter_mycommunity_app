"""快速测试 CORS 是否有重复值"""
import requests

def quick_test():
    print("🔍 快速测试 CORS 配置...")
    print("-" * 60)
    
    # 测试 OPTIONS
    url = "http://127.0.0.1:5000/Activity/searchMoreLikeActivity"
    headers = {
        'Origin': 'http://localhost:56824',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    print("测试 OPTIONS 预检请求:")
    response = requests.options(url, headers=headers)
    origin_header = response.headers.get('Access-Control-Allow-Origin', '')
    
    print(f"  状态码: {response.status_code}")
    print(f"  Access-Control-Allow-Origin: '{origin_header}'")
    
    # 检查是否有重复
    if ',' in origin_header:
        print(f"  ❌ 错误: 检测到重复的值 '{origin_header}'")
        print(f"  ⚠️  仍然有多处在添加 CORS 头!")
    elif origin_header == '*':
        print(f"  ✅ 正确: 单个值 '*'")
    else:
        print(f"  ⚠️  意外的值: '{origin_header}'")
    
    # 测试实际请求
    print("\n测试实际 POST 请求:")
    headers = {
        'Origin': 'http://localhost:56824',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json={'currIndex': 0}, headers=headers)
    origin_header = response.headers.get('Access-Control-Allow-Origin', '')
    
    print(f"  状态码: {response.status_code}")
    print(f"  Access-Control-Allow-Origin: '{origin_header}'")
    
    if ',' in origin_header:
        print(f"  ❌ 错误: 检测到重复的值")
    elif origin_header == '*':
        print(f"  ✅ 正确: 单个值 '*'")
    
    print("-" * 60)
    if ',' not in origin_header and origin_header == '*':
        print("✅ CORS 配置正确! 前端应该可以正常访问了")
    else:
        print("❌ CORS 仍有问题,需要进一步检查")

if __name__ == '__main__':
    quick_test()

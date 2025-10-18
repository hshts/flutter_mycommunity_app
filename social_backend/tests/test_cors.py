"""测试CORS配置"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_cors():
    """测试CORS配置"""
    print("=" * 60)
    print("测试CORS跨域配置")
    print("=" * 60)
    
    # 测试OPTIONS请求(预检请求)
    print("\n1. 测试OPTIONS预检请求")
    url = f"{BASE_URL}/Activity/getActivityTypeList"
    
    headers = {
        'Origin': 'http://localhost:49990',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    try:
        response = requests.options(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应头:")
        print(f"   - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"   - Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods')}")
        print(f"   - Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers')}")
        
        if response.headers.get('Access-Control-Allow-Origin'):
            print("   ✅ CORS配置正确")
        else:
            print("   ❌ CORS配置有问题")
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
    
    # 测试实际GET请求
    print("\n2. 测试实际GET请求")
    headers = {
        'Origin': 'http://localhost:49990'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应头:")
        print(f"   - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        if response.status_code == 200:
            print("   ✅ 请求成功")
        else:
            print(f"   ⚠️  状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
    
    # 测试POST请求
    print("\n3. 测试POST请求(动态列表)")
    url = f"{BASE_URL}/IM/getMomentList"
    headers = {
        'Origin': 'http://localhost:49990',
        'Content-Type': 'application/json'
    }
    data = {"currIndex": 0}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应头:")
        print(f"   - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        if response.status_code == 200:
            print("   ✅ POST请求成功")
        else:
            print(f"   ⚠️  状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ CORS测试完成")
    print("=" * 60)
    print("\n💡 提示: 如果所有测试都显示✅,说明CORS配置正确")
    print("   重启Flask服务器后,前端应该可以正常访问API了")

if __name__ == '__main__':
    test_cors()

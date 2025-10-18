"""详细测试 CORS 配置"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_cors_detailed():
    """详细测试 CORS 配置"""
    print("=" * 70)
    print("🔍 详细测试 CORS 跨域配置")
    print("=" * 70)
    
    # 测试 OPTIONS 预检请求
    print("\n【测试 1】OPTIONS 预检请求")
    print("-" * 70)
    url = f"{BASE_URL}/Activity/searchMoreLikeActivity"
    
    headers = {
        'Origin': 'http://localhost:56824',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    try:
        response = requests.options(url, headers=headers)
        print(f"📍 URL: {url}")
        print(f"📍 来源: http://localhost:56824")
        print(f"📍 状态码: {response.status_code}")
        print(f"\n响应头:")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
            'Access-Control-Max-Age': response.headers.get('Access-Control-Max-Age')
        }
        
        for key, value in cors_headers.items():
            if value:
                # 检查是否有重复值
                if ',' in str(value) and key == 'Access-Control-Allow-Origin':
                    print(f"  ❌ {key}: {value}")
                    print(f"      ⚠️  警告: 检测到重复的值!")
                else:
                    print(f"  ✅ {key}: {value}")
            else:
                print(f"  ❌ {key}: (缺失)")
        
        if response.status_code == 200:
            print("\n✅ OPTIONS 请求成功 (状态码 200)")
        else:
            print(f"\n❌ OPTIONS 请求失败 (状态码 {response.status_code})")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
    
    # 测试实际 POST 请求
    print("\n" + "=" * 70)
    print("【测试 2】实际 POST 请求")
    print("-" * 70)
    
    headers = {
        'Origin': 'http://localhost:56824',
        'Content-Type': 'application/json'
    }
    data = {"currIndex": 0}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"📍 URL: {url}")
        print(f"📍 来源: http://localhost:56824")
        print(f"📍 状态码: {response.status_code}")
        print(f"\n响应头:")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
        }
        
        for key, value in cors_headers.items():
            if value:
                # 检查是否有重复值
                if ',' in str(value) and key == 'Access-Control-Allow-Origin':
                    print(f"  ❌ {key}: {value}")
                    print(f"      ⚠️  警告: 检测到重复的值!")
                else:
                    print(f"  ✅ {key}: {value}")
            else:
                print(f"  ❌ {key}: (缺失)")
        
        if response.status_code == 200:
            print("\n✅ POST 请求成功")
        else:
            print(f"\n⚠️  POST 请求返回状态码 {response.status_code}")
            if response.text:
                print(f"响应内容: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
    
    # 测试动态列表接口
    print("\n" + "=" * 70)
    print("【测试 3】IM 动态列表接口")
    print("-" * 70)
    
    url = f"{BASE_URL}/IM/getMomentList"
    headers = {
        'Origin': 'http://localhost:56824',
        'Content-Type': 'application/json'
    }
    data = {"currIndex": 0}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"📍 URL: {url}")
        print(f"📍 状态码: {response.status_code}")
        
        allow_origin = response.headers.get('Access-Control-Allow-Origin')
        print(f"\n✅ Access-Control-Allow-Origin: {allow_origin}")
        
        # 检查是否有重复值
        if allow_origin and ',' in allow_origin:
            print(f"❌ 检测到重复的 CORS 头!")
        elif response.status_code == 200:
            print("✅ 请求成功,CORS 配置正确")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎉 测试完成")
    print("=" * 70)
    print("\n💡 提示:")
    print("   ✅ 如果所有 Access-Control-Allow-Origin 都显示单个值 '*'")
    print("   ✅ 且 OPTIONS 请求返回 200 状态码")
    print("   ✅ 则 CORS 配置正确,前端应该可以正常访问")
    print("\n   ❌ 如果出现 '*, *' 或其他重复值,说明有多处添加了 CORS 头")

if __name__ == '__main__':
    test_cors_detailed()

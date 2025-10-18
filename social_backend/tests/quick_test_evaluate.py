"""快速测试评价 API"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_evaluate():
    print("🧪 测试评价 API...")
    print("-" * 60)
    
    test_goodpriceid = "5cee1569-4dad-415c-a350-2482cd629d48"
    url = f"{BASE_URL}/grouppurchase/getEvaluateGoodPriceList"
    
    response = requests.post(url, json={"goodpriceid": test_goodpriceid, "currentIndex": 0}, 
                            headers={'Content-Type': 'application/json'})
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        evaluates = result.get('data', [])
        print(f"✅ 获取到 {len(evaluates)} 条评价")
        
        if evaluates:
            first = evaluates[0]
            evaluateid = first.get('evaluateid')
            print(f"\n第一条评价:")
            print(f"  evaluateid: {evaluateid} (类型: {type(evaluateid).__name__})")
            print(f"  评分: {'⭐' * first.get('liketype')} ({first.get('liketype')}星)")
            print(f"  内容: {first.get('content')}")
            
            if isinstance(evaluateid, int):
                print(f"\n✅ evaluateid 是 Integer 类型!")
            else:
                print(f"\n⚠️  evaluateid 不是 Integer")
    else:
        print(f"❌ 请求失败: {response.text}")

if __name__ == '__main__':
    test_evaluate()

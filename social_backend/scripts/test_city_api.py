#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：根据城市获取活动列表接口

运行方式：
1. 启动 Flask 应用：flask run
2. 运行此脚本：python scripts/test_city_api.py
"""

import requests
import json

# API 基础URL
BASE_URL = "http://127.0.0.1:5000"

def print_response(response, title):
    """打印响应结果"""
    print(f"\n{'='*60}")
    print(f"测试：{title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*60}\n")

def test_basic_query():
    """测试基本查询"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    params = {
        "citycode": "440300"  # 深圳
    }
    response = requests.get(url, params=params)
    print_response(response, "基本查询 - 获取深圳的活动")
    return response.status_code == 200

def test_pagination():
    """测试分页"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    params = {
        "citycode": "440300",
        "currentIndex": 0,
        "pageSize": 5
    }
    response = requests.get(url, params=params)
    print_response(response, "分页查询 - 第一页，每页5条")
    return response.status_code == 200

def test_order_by_likes():
    """测试按点赞数排序"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    params = {
        "citycode": "440300",
        "orderBy": "likenum"
    }
    response = requests.get(url, params=params)
    print_response(response, "排序查询 - 按点赞数排序")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            likes = [act['likenum'] for act in data['data']]
            print(f"点赞数列表: {likes}")
            is_sorted = likes == sorted(likes, reverse=True)
            print(f"是否正确排序: {'✅' if is_sorted else '❌'}")
            return is_sorted
    return False

def test_order_by_views():
    """测试按浏览数排序"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    params = {
        "citycode": "440300",
        "orderBy": "viewnum"
    }
    response = requests.get(url, params=params)
    print_response(response, "排序查询 - 按浏览数排序")
    return response.status_code == 200

def test_missing_citycode():
    """测试缺少必填参数"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    response = requests.get(url)
    print_response(response, "参数验证 - 缺少citycode")
    return response.status_code == 400

def test_invalid_order_by():
    """测试无效的排序字段"""
    url = f"{BASE_URL}/Activity/getActivityListByCity"
    params = {
        "citycode": "440300",
        "orderBy": "invalid_field"
    }
    response = requests.get(url, params=params)
    print_response(response, "参数验证 - 无效的排序字段（应自动使用默认值）")
    return response.status_code == 200

def main():
    """主测试函数"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   测试接口: 根据城市获取活动列表 (API 2.25)              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("基本查询", test_basic_query),
        ("分页查询", test_pagination),
        ("按点赞数排序", test_order_by_likes),
        ("按浏览数排序", test_order_by_views),
        ("参数验证-缺少citycode", test_missing_citycode),
        ("参数验证-无效排序字段", test_invalid_order_by),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ 连接失败！请确保 Flask 应用正在运行：flask run")
            return
        except Exception as e:
            print(f"\n❌ 测试失败: {test_name}")
            print(f"错误信息: {str(e)}")
            results.append((test_name, False))
    
    # 打印测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    print("="*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！接口工作正常。")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查。")

if __name__ == "__main__":
    main()

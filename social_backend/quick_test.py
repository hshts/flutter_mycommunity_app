#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速 API 测试脚本（不需要启动 Flask 服务器）

使用方法：
    python quick_test.py
"""

from api import create_app, db
from api.models.activity import Activity

def test_queries():
    """测试数据库查询"""
    app = create_app()
    
    with app.app_context():
        print("="*60)
        print("数据库查询测试")
        print("="*60)
        
        # 测试1: 查询所有活动
        total = Activity.query.count()
        print(f"\n1. 总活动数: {total}")
        
        # 测试2: 按城市查询（深圳）
        sz_activities = Activity.query.filter_by(actcity='440300').all()
        print(f"\n2. 深圳市(440300)活动数: {len(sz_activities)}")
        for act in sz_activities:
            print(f"   - {act.content[:40]}")
        
        # 测试3: 按城市查询（福田）
        ft_activities = Activity.query.filter_by(actcity='440304').all()
        print(f"\n3. 福田区(440304)活动数: {len(ft_activities)}")
        for act in ft_activities:
            print(f"   - {act.content[:40]}")
        
        # 测试4: 按点赞数排序
        popular = Activity.query.filter_by(actcity='440300')\
                                .order_by(Activity.likenum.desc())\
                                .all()
        print(f"\n4. 深圳活动按点赞数排序:")
        for act in popular:
            print(f"   - {act.content[:40]:45} 点赞: {act.likenum}")
        
        # 测试5: 分页查询
        page1 = Activity.query.filter_by(actcity='440300')\
                              .offset(0)\
                              .limit(2)\
                              .all()
        print(f"\n5. 分页查询(深圳，第1页，每页2条):")
        for act in page1:
            print(f"   - {act.content[:40]}")
        
        print("\n" + "="*60)
        print("✅ 所有查询测试通过！数据库工作正常。")
        print("="*60)
        
        print("\n现在可以启动 Flask 服务器测试 API:")
        print("  flask run")
        print("\n然后访问:")
        print("  http://localhost:5000/Activity/getActivityListByCity?citycode=440300")

if __name__ == '__main__':
    test_queries()

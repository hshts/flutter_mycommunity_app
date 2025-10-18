#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加测试数据脚本

使用方法：
    python scripts/add_activity_test_data.py
"""

# 确保可以从脚本直接运行时导入 api 包
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api import create_app, db
from api.models.activity import Activity
from datetime import datetime
import uuid

def add_test_data():
    """添加测试数据"""
    app = create_app()
    
    with app.app_context():
        print("正在添加测试数据...")
        
        # 测试活动数据
        test_activities = [
            {
                'actid': f'act_{uuid.uuid4().hex[:16]}',
                'content': '深圳周末户外徒步活动 - 梧桐山登山',
                'uid': 1001,
                'actprovince': '440000',
                'actcity': '440300',
                'address': '深圳市罗湖区梧桐山风景区',
                'addresstitle': '梧桐山风景区',
                'lat': 22.5963,
                'lng': 114.1901,
                'coverimg': 'https://example.com/wutong.jpg',
                'coverimgwh': '800x600',
                'startyear': 1729238400,  # 2024-10-18
                'endyear': 1729324800,    # 2024-10-19
                'paytype': 0,
                'peoplenum': 20,
                'currentpeoplenum': 8,
                'likenum': 125,
                'collectionnum': 68,
                'commentnum': 42,
                'viewnum': 2580,
                'joinnum': 8,
                'status': 1
            },
            {
                'actid': f'act_{uuid.uuid4().hex[:16]}',
                'content': '深圳湾骑行活动 - 欢迎新手参加',
                'uid': 1002,
                'actprovince': '440000',
                'actcity': '440300',
                'address': '深圳市南山区深圳湾公园',
                'addresstitle': '深圳湾公园',
                'lat': 22.5134,
                'lng': 113.9339,
                'coverimg': 'https://example.com/bay.jpg',
                'coverimgwh': '800x600',
                'startyear': 1729324800,
                'endyear': 1729411200,
                'paytype': 0,
                'peoplenum': 15,
                'currentpeoplenum': 12,
                'likenum': 89,
                'collectionnum': 45,
                'commentnum': 28,
                'viewnum': 1850,
                'joinnum': 12,
                'status': 1
            },
            {
                'actid': f'act_{uuid.uuid4().hex[:16]}',
                'content': '南山科技园周末羽毛球活动',
                'uid': 1003,
                'actprovince': '440000',
                'actcity': '440300',
                'address': '深圳市南山区科技园体育中心',
                'addresstitle': '科技园体育中心',
                'lat': 22.5431,
                'lng': 113.9434,
                'coverimg': 'https://example.com/badminton.jpg',
                'coverimgwh': '800x600',
                'startyear': 1729411200,
                'endyear': 1729497600,
                'paytype': 1,
                'mincost': 30.0,
                'maxcost': 50.0,
                'peoplenum': 8,
                'currentpeoplenum': 6,
                'likenum': 56,
                'collectionnum': 32,
                'commentnum': 15,
                'viewnum': 980,
                'joinnum': 6,
                'status': 1
            },
            {
                'actid': f'act_{uuid.uuid4().hex[:16]}',
                'content': '北京周末爬香山活动',
                'uid': 2001,
                'actprovince': '110000',
                'actcity': '110100',
                'address': '北京市海淀区香山公园',
                'addresstitle': '香山公园',
                'lat': 39.9917,
                'lng': 116.1886,
                'coverimg': 'https://example.com/xiangshan.jpg',
                'coverimgwh': '800x600',
                'startyear': 1729238400,
                'endyear': 1729324800,
                'paytype': 1,
                'mincost': 10.0,
                'maxcost': 10.0,
                'peoplenum': 30,
                'currentpeoplenum': 18,
                'likenum': 234,
                'collectionnum': 128,
                'commentnum': 76,
                'viewnum': 4520,
                'joinnum': 18,
                'status': 1
            },
            {
                'actid': f'act_{uuid.uuid4().hex[:16]}',
                'content': '福田中心区周末跑步团',
                'uid': 1004,
                'actprovince': '440000',
                'actcity': '440304',  # 福田区
                'address': '深圳市福田区莲花山公园',
                'addresstitle': '莲花山公园',
                'lat': 22.5486,
                'lng': 114.0547,
                'coverimg': 'https://example.com/lianhua.jpg',
                'coverimgwh': '800x600',
                'startyear': 1729152000,
                'endyear': 1729238400,
                'paytype': 0,
                'peoplenum': 25,
                'currentpeoplenum': 15,
                'likenum': 178,
                'collectionnum': 92,
                'commentnum': 54,
                'viewnum': 3120,
                'joinnum': 15,
                'status': 1
            },
        ]
        
        # 添加活动到数据库
        for activity_data in test_activities:
            activity = Activity(**activity_data)
            db.session.add(activity)
            print(f"  ✓ 添加活动: {activity_data['content'][:30]}...")
        
        db.session.commit()
        
        # 统计数据
        total = Activity.query.count()
        shenzhen_count = Activity.query.filter_by(actcity='440300').count()
        futian_count = Activity.query.filter_by(actcity='440304').count()
        beijing_count = Activity.query.filter_by(actcity='110100').count()
        
        print(f"\n✅ 测试数据添加完成！")
        print(f"\n数据统计:")
        print(f"  - 总活动数: {total}")
        print(f"  - 深圳市(440300): {shenzhen_count}")
        print(f"  - 福田区(440304): {futian_count}")
        print(f"  - 北京市(110100): {beijing_count}")
        
        print(f"\n可以测试的城市代码:")
        print(f"  - 440300 (深圳市)")
        print(f"  - 440304 (福田区)")
        print(f"  - 110100 (北京市)")

if __name__ == '__main__':
    add_test_data()

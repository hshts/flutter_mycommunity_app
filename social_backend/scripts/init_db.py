#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本

使用方法：
    python init_db.py
"""

from api import create_app, db
from api.models.activity import Activity

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        print("正在创建数据库表...")
        
        # 删除所有表（如果存在）
        db.drop_all()
        print("✓ 已删除旧表")
        
        # 创建所有表
        db.create_all()
        print("✓ 已创建新表")
        
        # 验证表是否创建成功
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n已创建的表: {', '.join(tables)}")
        
        # 显示 activities 表的结构
        if 'activities' in tables:
            print("\n✓ activities 表结构:")
            columns = inspector.get_columns('activities')
            for column in columns:
                print(f"  - {column['name']}: {column['type']}")
        
        print("\n✅ 数据库初始化完成！")

if __name__ == '__main__':
    init_database()

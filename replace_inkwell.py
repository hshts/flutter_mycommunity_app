#!/usr/bin/env python3
"""
批量将 InkWell 替换为 GestureDetector 的脚本
用于优化 Flutter 项目的 web 端性能
"""

import os
import re
import sys
from pathlib import Path

def replace_inkwell_with_gesturedetector(file_path):
    """将文件中的 InkWell 替换为 GestureDetector"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 简单的字符串替换
        content = content.replace('InkWell(', 'GestureDetector(')
        content = content.replace('return InkWell(', 'return GestureDetector(')
        content = content.replace('= InkWell(', '= GestureDetector(')
        content = content.replace(': InkWell(', ': GestureDetector(')
        content = content.replace('child: InkWell(', 'child: GestureDetector(')
        content = content.replace('? InkWell(', '? GestureDetector(')
        content = content.replace('InkWell\n', 'GestureDetector\n')
        content = content.replace('\nInkWell(', '\nGestureDetector(')
        content = content.replace('=> InkWell(', '=> GestureDetector(')
        content = content.replace('leading: InkWell(', 'leading: GestureDetector(')
        content = content.replace('title: InkWell(', 'title: GestureDetector(')
        content = content.replace('center: InkWell(', 'center: GestureDetector(')
        content = content.replace('bottomNavigationBar: InkWell(', 'bottomNavigationBar: GestureDetector(')
        
        # 检查是否有修改
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """主函数"""
    lib_path = Path("lib")
    
    if not lib_path.exists():
        print("lib 目录不存在")
        return
    
    dart_files = list(lib_path.rglob("*.dart"))
    print(f"找到 {len(dart_files)} 个 Dart 文件")
    
    modified_files = []
    
    for dart_file in dart_files:
        if replace_inkwell_with_gesturedetector(dart_file):
            modified_files.append(dart_file)
            print(f"已修改: {dart_file}")
    
    print(f"\n总共修改了 {len(modified_files)} 个文件:")
    for file in modified_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
客户端启动脚本
用于直接运行 PySide6 客户端应用
"""
import sys
import os

# 将当前目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 直接运行client/main.py
    from client import main